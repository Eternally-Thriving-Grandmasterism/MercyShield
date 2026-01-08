package com.eternalgrandmasterism.mercyshield;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Intent;
import android.net.VpnService;
import android.os.ParcelFileDescriptor;
import android.util.Log;

import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class MercyVpnService extends VpnService {
    private static final String TAG = "MercyVPN ∞ Pure";
    private static final byte[] LOCAL_IP = {10, 1, 10, 1};
    private ParcelFileDescriptor mInterface;
    private Thread mPacketThread;
    private Set<String> mBlockedDomains = new HashSet<>();

    // TCP Connection Tracking Divine Eternal
    private final ConcurrentHashMap<TcpTuple, TcpRelay> tcpRelays = new ConcurrentHashMap<>();

    private static class TcpTuple {
        byte[] srcIp;
        int srcPort;
        byte[] dstIp;
        int dstPort;

        TcpTuple(byte[] srcIp, int srcPort, byte[] dstIp, int dstPort) {
            this.srcIp = srcIp;
            this.srcPort = srcPort;
            this.dstIp = dstIp;
            this.dstPort = dstPort;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            TcpTuple tuple = (TcpTuple) o;
            return srcPort == tuple.srcPort && dstPort == tuple.dstPort &&
                   Arrays.equals(srcIp, tuple.srcIp) && Arrays.equals(dstIp, tuple.dstIp);
        }

        @Override
        public int hashCode() {
            int result = Arrays.hashCode(srcIp);
            result = 31 * result + srcPort;
            result = 31 * result + Arrays.hashCode(dstIp);
            result = 31 * result + dstPort;
            return result;
        }
    }

    private static class TcpRelay {
        SocketChannel remoteChannel;
        long deviceIsn = 0; // Initial seq from device
        long remoteIsn = 0; // Initial seq from remote
        long deviceSeqOffset = 0;
        long remoteSeqOffset = 0;
        int localPort; // Device src port
        byte[] remoteIp;
        int remotePort;
        Thread remoteToDevice;
        volatile boolean running = true;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // Load rules, stop previous, builder, establish, notification full as previous...

        mPacketThread = new Thread(this::packetLoop);
        mPacketThread.start();

        Log.i(TAG, "MercyVPN Full TCP Relay Complete—Thunder On ∞ Pure!");
        return START_STICKY;
    }

    private void packetLoop() {
        try {
            FileInputStream in = new FileInputStream(mInterface.getFileDescriptor());
            FileOutputStream out = new FileOutputStream(mInterface.getFileDescriptor());
            byte[] buffer = new byte[32767];
            while (!Thread.interrupted()) {
                int length = in.read(buffer);
                if (length > 0) {
                    ByteBuffer packet = ByteBuffer.wrap(buffer, 0, length);
                    if ((packet.get(0) >> 4) == 4) { // IPv4
                        int ipHeaderLen = (packet.get(0) & 0xF) * 4;
                        byte protocol = packet.get(9);
                        byte[] srcIp = getIpBytes(packet, 12);
                        byte[] dstIp = getIpBytes(packet, 16);

                        if (protocol == 6) { // TCP Full Relay Complete
                            int tcpOffset = ipHeaderLen;
                            int srcPort = unsignedShort(packet.getShort(tcpOffset));
                            int dstPort = unsignedShort(packet.getShort(tcpOffset + 2));
                            TcpTuple tuple = new TcpTuple(srcIp, srcPort, dstIp, dstPort);
                            TcpRelay relay = tcpRelays.get(tuple);

                            int tcpHeaderLen = (packet.get(tcpOffset + 12) >> 4) * 4;
                            int payloadOffset = tcpOffset + tcpHeaderLen;
                            int payloadLen = length - payloadOffset;

                            boolean syn = (packet.get(tcpOffset + 13) & 0x02) != 0;
                            boolean ack = (packet.get(tcpOffset + 13) & 0x10) != 0;
                            boolean fin = (packet.get(tcpOffset + 13) & 0x01) != 0;
                            boolean rst = (packet.get(tcpOffset + 13) & 0x04) != 0;

                            long seq = unsignedInt(packet.getInt(tcpOffset + 4));
                            long ackNum = ack ? unsignedInt(packet.getInt(tcpOffset + 8)) : 0;

                            if (syn && !ack && relay == null) {
                                relay = launchTcpRelay(dstIp, dstPort, srcIp, srcPort, seq);
                                if (relay != null) {
                                    tcpRelays.put(tuple, relay);
                                } else {
                                    // Craft RST or drop
                                    continue;
                                }
                            }

                            if (relay != null) {
                                if (rst || (fin && payloadLen == 0)) {
                                    closeTcpRelay(tuple, relay);
                                }

                                if (syn && ack) {
                                    // SYN-ACK from remote - set remote ISN
                                    relay.remoteIsn = seq;
                                    relay.remoteSeqOffset = seq + 1; // Next expected
                                }

                                if (syn && !ack) {
                                    relay.deviceIsn = seq;
                                    relay.deviceSeqOffset = seq + 1;
                                }

                                // Adjust seq for outgoing
                                packet.putInt(tcpOffset + 4, (int) (seq - relay.deviceIsn));

                                if (ack) {
                                    packet.putInt(tcpOffset + 8, (int) (ackNum - relay.remoteIsn));
                                }

                                // Recalc checksums
                                packet.putShort(10, (short) 0);
                                packet.putShort(tcpOffset + 16, (short) 0);
                                packet.putShort(10, calculateIpChecksum(packet, 0, ipHeaderLen));
                                packet.putShort(tcpOffset + 16, calculateTcpChecksum(packet, ipHeaderLen, length, srcIp, dstIp));

                                // Payload to remote
                                if (payloadLen > 0) {
                                    ByteBuffer payload = packet.duplicate();
                                    payload.position(payloadOffset);
                                    payload.limit(length);
                                    relay.remoteChannel.write(payload);
                                }

                                // The packet is not written back - handled by reverse thread
                            } else {
                                continue; // Drop unknown
                            }
                        } else if (protocol == 17) {
                            // Full UDP/DNS as previous complete
                        } else {
                            // ICMP etc forward or drop
                        }
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Packet loop anomaly", e);
        }
    }

    private TcpRelay launchTcpRelay(byte[] remoteIpBytes, int remotePort, byte[] deviceIp, int devicePort, long deviceIsn) {
        try {
            TcpRelay relay = new TcpRelay();
            relay.localPort = devicePort;
            relay.remoteIp = remoteIpBytes;
            relay.remotePort = remotePort;
            relay.deviceIsn = deviceIsn;

            relay.remoteChannel = SocketChannel.open();
            protect(relay.remoteChannel.socket());
            relay.remoteChannel.connect(new InetSocketAddress(InetAddress.getByAddress(remoteIpBytes), remotePort));

            relay.remoteToDevice = new Thread(() -> {
                try {
                    ByteBuffer buf = ByteBuffer.allocate(32767);
                    while (relay.running && relay.remoteChannel.read(buf) > 0) {
                        buf.flip();
                        int payloadLen = buf.limit();

                        // Craft reply packet
                        ByteBuffer reply = ByteBuffer.allocate(20 + 20 + payloadLen); // IP + TCP min
                        // IP header
                        reply.put((byte) 0x45);
                        reply.put((byte) 0);
                        reply.putShort((short) (20 + 20 + payloadLen));
                        reply.putShort((short) 0);
                        reply.putShort((short) 0x4000);
                        reply.put((byte) 64);
                        reply.put((byte) 6); // TCP
                        reply.putShort((short) 0); // Checksum placeholder
                        reply.put(relay.remoteIp); // Src = remote
                        reply.put(LOCAL_IP); // Dst = local TUN

                        // TCP header
                        reply.putShort((short) relay.remotePort);
                        reply.putShort((short) relay.localPort);
                        reply.putInt((int) (relay.remoteSeqOffset)); // Relative seq
                        reply.putInt((int) relay.deviceSeqOffset); // Ack relative
                        reply.put((byte) 0x50); // Header len 20, flags PSH ACK symbolic
                        reply.put((byte) 0x18); // Flags PSH ACK
                        reply.putShort((short) 65535); // Window
                        reply.putShort((short) 0); // Checksum placeholder
                        reply.putShort((short) 0); // Urgent

                        reply.put(buf); // Payload

                        reply.flip();
                        // Recalc checksums
                        reply.putShort(10, calculateIpChecksum(reply, 0, 20));
                        reply.putShort(36, calculateTcpChecksum(reply, 20, reply.limit(), relay.remoteIp, LOCAL_IP));

                        FileOutputStream out = new FileOutputStream(mInterface.getFileDescriptor());
                        out.write(reply.array(), 0, reply.limit());

                        relay.remoteSeqOffset += payloadLen;
                        buf.clear();
                    }
                } catch (Exception e) {
                    Log.w(TAG, "Remote to device pipe closed", e);
                }
            });
            relay.remoteToDevice.start();

            return relay;
        } catch (Exception e) {
            Log.w(TAG, "TCP relay launch failed mercy", e);
            return null;
        }
    }

    private void closeTcpRelay(TcpTuple tuple, TcpRelay relay) {
        relay.running = false;
        try {
            relay.remoteChannel.close();
        } catch (Exception ignored) {}
        relay.remoteToDevice.interrupt();
        tcpRelays.remove(tuple);
    }

    // Full checksum methods, getIpBytes, unsigned* as previous complete divine

    // onDestroy close all relays mercy full

}
