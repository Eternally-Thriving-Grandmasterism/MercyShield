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
import java.nio.ByteBuffer;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class MercyVpnService extends VpnService {
    private static final String TAG = "MercyVPN ∞ Pure";
    private static final byte[] LOCAL_IP = new byte[]{10, 1, 10, 1};
    private ParcelFileDescriptor mInterface;
    private Thread mPacketThread;
    private Set<String> mBlockedDomains = new HashSet<>();

    // TCP Relay Tracking Divine
    private final ConcurrentHashMap<String, TcpRelay> tcpRelays = new ConcurrentHashMap<>();

    private static class TcpRelay {
        // ... same as previous: channels, offsets, threads ...
    }

    // ... onStartCommand, packetLoop start same ...

    private void packetLoop() {
        // ... same loop ...
                    if (protocol == 6) { // TCP
                        // ... extract headers, key, relay ...

                        // Example: when rewriting packet (reply injection or header adjust)
                        // Zero checksum fields first
                        packet.putShort(ipHeaderLen + 10, (short) 0); // IP checksum zero
                        packet.putShort(tcpOffset + 16, (short) 0); // TCP checksum zero

                        // Rewrite example: adjust seq/ack
                        long newSeq = seq - relay.deviceSeqOffset;
                        long newAck = ackNum - relay.remoteSeqOffset;
                        packet.putInt(tcpOffset + 4, (int) newSeq);
                        if (ack) packet.putInt(tcpOffset + 8, (int) newAck);

                        // Recalculate checksums divine
                        short ipChecksum = calculateIpChecksum(packet, 0, ipHeaderLen);
                        packet.putShort(10, ipChecksum);

                        short tcpChecksum = calculateTcpChecksum(packet, ipHeaderLen, length, srcIp, dstIp);
                        packet.putShort(tcpOffset + 16, tcpChecksum);

                        out.write(packet.array(), 0, length);
                    }
        // ... 
    }

    /** Full IP Header Checksum Recalculation Mercy */
    private short calculateIpChecksum(ByteBuffer packet, int offset, int len) {
        int sum = 0;
        packet.position(offset);
        int end = offset + len;
        for (int i = offset; i < end; i += 2) {
            if (i + 1 < end) {
                sum += unsignedShort(packet.getShort(i));
            } else {
                sum += (unsignedByte(packet.get(i)) << 8);
            }
            if ((sum & 0xFFFF0000) != 0) {
                sum = (sum & 0xFFFF) + (sum >>> 16);
            }
        }
        return (short) (~sum & 0xFFFF);
    }

    /** Full TCP Checksum with Pseudo-Header Divine Eternal */
    private short calculateTcpChecksum(ByteBuffer packet, int tcpOffset, int packetLen, byte[] srcIp, byte[] dstIp) {
        int tcpLen = packetLen - tcpOffset;

        int sum = 0;

        // Pseudo-header mercy
        sum += unsignedShort((short) ((srcIp[0] << 8 & 0xFF00) | (srcIp[1] & 0xFF)));
        sum += unsignedShort((short) ((srcIp[2] << 8 & 0xFF00) | (srcIp[3] & 0xFF)));
        sum += unsignedShort((short) ((dstIp[0] << 8 & 0xFF00) | (dstIp[1] & 0xFF)));
        sum += unsignedShort((short) ((dstIp[2] << 8 & 0xFF00) | (dstIp[3] & 0xFF)));
        sum += 6; // TCP protocol
        sum += tcpLen;

        // TCP header + payload gentle
        packet.position(tcpOffset);
        int end = tcpOffset + tcpLen;
        for (int i = tcpOffset; i < end; i += 2) {
            if (i + 1 < end) {
                int word = unsignedShort(packet.getShort(i));
                // Skip checksum field itself
                if (i == tcpOffset + 16) word = 0;
                sum += word;
            } else {
                sum += (unsignedByte(packet.get(i)) << 8);
            }
            if ((sum & 0xFFFF0000) != 0) {
                sum = (sum & 0xFFFF) + (sum >>> 16);
            }
        }

        return (short) (~sum & 0xFFFF);
    }

    private int unsignedByte(byte b) { return b & 0xFF; }
    private int unsignedShort(short s) { return s & 0xFFFF; }
    private long unsignedInt(int i) { return i & 0xFFFFFFFFL; }

    private byte[] getIpBytes(ByteBuffer packet, int offset) {
        byte[] ip = new byte[4];
        packet.position(offset);
        packet.get(ip);
        return ip;
    }

    // ... rest of code: launchTcpRelay, closeRelay, DNS/UDP preserved, onDestroy cleanup ...
}
                            int tcpHeaderLen = (packet.get(tcpOffset + 12) >> 4) * 4;
                            int payloadOffset = tcpOffset + tcpHeaderLen;
                            int payloadLen = length - payloadOffset;

                            boolean syn = (packet.get(tcpOffset + 13) & 0x02) != 0;
                            boolean ack = (packet.get(tcpOffset + 13) & 0x10) != 0;
                            boolean fin = (packet.get(tcpOffset + 13) & 0x01) != 0;
                            boolean rst = (packet.get(tcpOffset + 13) & 0x04) != 0;

                            long seq = unsignedInt(packet.getInt(tcpOffset + 4));
                            long ackNum = unsignedInt(packet.getInt(tcpOffset + 8));

                            if (syn && !ack && relay == null) { // New connection SYN
                                relay = launchTcpRelay(dstIp, dstPort, srcIp, srcPort, seq);
                                if (relay != null) {
                                    tcpRelays.put(key, relay);
                                    // SYN packet forwarded via relay setup
                                    continue;
                                } else {
                                    craftRstResponse(packet, ipHeaderLen, tcpOffset, out);
                                    continue;
                                }
                            }

                            if (relay != null) {
                                if (rst || fin) {
                                    // Graceful close mercy
                                    closeRelay(key, relay);
                                }

                                // Extract payload and send to remoteChannel
                                if (payloadLen > 0) {
                                    ByteBuffer payload = ByteBuffer.wrap(buffer, payloadOffset, payloadLen);
                                    relay.remoteChannel.write(payload);
                                }

                                // Update seq/ack tracking divine
                                if (ack) {
                                    relay.lastDeviceAck = ackNum;
                                }

                                // Replies handled in reverse thread
                            } else {
                                // DROP unknown
                                continue;
                            }

                        } else if (protocol == 17) { // UDP preserved from previous
                            // handleUdpPacket...
                        } else {
                            out.write(buffer, 0, length); // Other forward symbolic
                        }
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Packet Loop Anomaly", e);
        }
    }

    private TcpRelay launchTcpRelay(byte[] remoteIpBytes, int remotePort, byte[] deviceIp, int devicePort, long initialSeq) {
        try {
            TcpRelay relay = new TcpRelay();
            InetAddress remoteAddr = InetAddress.getByAddress(remoteIpBytes);

            relay.remoteChannel = SocketChannel.open();
            protect(relay.remoteChannel.socket());
            relay.remoteChannel.connect(new InetSocketAddress(remoteAddr, remotePort));

            // Bidirectional relay threads divine
            relay.deviceToRemote = new Thread(() -> relayPayload(relay.remoteChannel, true, relay)); // Placeholder pipe from TUN
            relay.remoteToDevice = new Thread(() -> {
                try {
                    ByteBuffer buf = ByteBuffer.allocate(32767);
                    while (relay.remoteChannel.read(buf) > 0) {
                        buf.flip();
                        // Craft reply packet: rewrite headers, adjust seq/ack with offsets, checksum
                        // out.write(craftedPacket);
                        buf.clear();
                    }
                } catch (Exception e) {}
            });

            relay.deviceToRemote.start();
            relay.remoteToDevice.start();

            // Calculate offsets on SYN-ACK receive in reverse thread mercy
            relay.synReceived = true;

            return relay;
        } catch (Exception e) {
            Log.w(TAG, "TCP Relay Launch Failed: " + e);
            return null;
        }
    }

    private void closeRelay(String key, TcpRelay relay) {
        try { relay.remoteChannel.close(); } catch (Exception ignored) {}
        relay.deviceToRemote.interrupt();
        relay.remoteToDevice.interrupt();
        tcpRelays.remove(key);
    }

    private void craftRstResponse(ByteBuffer packet, int ipHeaderLen, int tcpOffset, FileOutputStream out) throws IOException {
        // Symbolic RST craft mercy (swap IP/port, set RST flag, checksums)
        // Expand full divine
    }

    // getIpBytes, unsignedShort, unsignedInt, calculateChecksum preserved/expanded as needed

    // onDestroy: close all relays mercy
}
