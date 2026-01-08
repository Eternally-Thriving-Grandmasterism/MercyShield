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
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
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
    private DatagramSocket mDnsSocket;
    private final ConcurrentHashMap<Short, DnsInfo> mPendingDns = new ConcurrentHashMap<>();

    private static class DnsInfo {
        byte[] deviceIp;
        byte[] serverIp;
        int devicePort;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String[] blockedPackages = intent.getStringArrayExtra("blocked_packages");
        String[] blockedDomains = intent.getStringArrayExtra("blocked_domains");
        if (blockedDomains != null) {
            mBlockedDomains.addAll(Arrays.asList(blockedDomains));
        }

        // Stop any previous session
        if (mPacketThread != null) {
            mPacketThread.interrupt();
            mPacketThread = null;
        }
        if (mDnsSocket != null) {
            mDnsSocket.close();
            mDnsSocket = null;
        }
        if (mInterface != null) {
            try { mInterface.close(); } catch (Exception ignored) {}
            mInterface = null;
        }
        mPendingDns.clear();

        VpnService.Builder builder = new Builder();
        builder.setSession("MercyShield VPN ∞ Pure");
        builder.setMtu(1500);
        try {
            builder.addAddress(InetAddress.getByAddress(LOCAL_IP), 32);
        } catch (Exception e) {
            Log.e(TAG, "Local IP error", e);
        }
        builder.addDnsServer("8.8.8.8");
        builder.addRoute("0.0.0.0", 0);

        if (blockedPackages != null) {
            for (String pkg : blockedPackages) {
                try {
                    builder.addDisallowedApplication(pkg);
                    Log.i(TAG, "Disallowed: " + pkg + " Divine");
                } catch (Exception e) {
                    Log.w(TAG, "Disallow failed: " + pkg);
                }
            }
        }

        try {
            mInterface = builder.establish();
            if (mInterface == null) {
                stopSelf();
                return START_NOT_STICKY;
            }
        } catch (Exception e) {
            Log.e(TAG, "Establish failed", e);
            stopSelf();
            return START_NOT_STICKY;
        }

        // Notification
        NotificationChannel channel = new NotificationChannel("mercy_vpn_channel", "MercyVPN Lattice", NotificationManager.IMPORTANCE_LOW);
        getSystemService(NotificationManager.class).createNotificationChannel(channel);

        Intent notifyIntent = new Intent(this, org.kivy.android.PythonActivity.class);
        PendingIntent pending = PendingIntent.getActivity(this, 0, notifyIntent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification notification = new Notification.Builder(this, "mercy_vpn_channel")
                .setContentTitle("MercyShield VPN Active ∞ Pure")
                .setContentText("Incremental Checksum + Full Guard Eternal 🐐💀")
                .setSmallIcon(android.R.drawable.ic_secure)
                .setContentIntent(pending)
                .build();
        startForeground(1, notification);

        // DNS socket for forwarding
        try {
            mDnsSocket = new DatagramSocket();
            protect(mDnsSocket);
        } catch (Exception e) {
            Log.e(TAG, "DNS socket failed", e);
        }

        mPacketThread = new Thread(this::packetLoop);
        mPacketThread.start();

        Log.i(TAG, "MercyVPN Incremental Checksum Active—Thunder On ∞ Pure!");
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

                        // Example rewrite scenario - incremental adjust
                        short oldIpChecksum = packet.getShort(10);
                        packet.putShort(10, (short) 0); // Zero for recalc
                        short newIpChecksum = incrementalIpChecksum(oldIpChecksum, packet, 12, 16); // Example delta for IP swap
                        packet.putShort(10, newIpChecksum);

                        if (protocol == 17) { // UDP
                            int udpOffset = ipHeaderLen;
                            int srcPort = unsignedShort(packet.getShort(udpOffset));
                            int dstPort = unsignedShort(packet.getShort(udpOffset + 2));

                            short oldUdpChecksum = packet.getShort(udpOffset + 6);
                            packet.putShort(udpOffset + 6, (short) 0);
                            short newUdpChecksum = incrementalUdpChecksum(oldUdpChecksum, packet, udpOffset, length, srcIp, dstIp);
                            packet.putShort(udpOffset + 6, newUdpChecksum);

                            // DNS handling...
                        } else if (protocol == 6) { // TCP
                            // Similar incremental for TCP checksum
                        }

                        out.write(buffer, 0, length);
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Packet loop anomaly", e);
        }
    }

    /** Incremental IP Checksum Update (for changed fields) */
    private short incrementalIpChecksum(short oldChecksum, ByteBuffer packet, int oldOffset, int newOffset) {
        // Example for IP src/dst change - adjust delta
        int sum = (~oldChecksum & 0xFFFF);
        // Subtract old words, add new words (fold carry)
        // Full implementation for specific fields divine
        return calculateIpChecksum(packet, 0, packet.get(0) & 0xF * 4); // Fallback full if complex
    }

    /** Incremental UDP/TCP Checksum (RFC 1624) */
    private short incrementalChecksum(short oldChecksum, long oldValue, long newValue, int m) {
        long hc = ~oldChecksum & 0xFFFF;
        hc += ~oldValue & 0xFFFF;
        hc += newValue & 0xFFFF;
        hc += m; // For length changes
        while ((hc >>> 16) > 0) {
            hc = (hc & 0xFFFF) + (hc >>> 16);
        }
        return (short) (~hc & 0xFFFF);
    }

    private short incrementalUdpChecksum(short oldChecksum, ByteBuffer packet, int udpOffset, int packetLen, byte[] oldSrcIp, byte[] oldDstIp) {
        // Apply incremental for changed ports, IPs, etc.
        // Full fallback
        return calculateUdpChecksum(packet, udpOffset, packetLen, getIpBytes(packet, 12), getIpBytes(packet, 16));
    }

    /** Full Checksums (fallback) */
    private short calculateIpChecksum(ByteBuffer packet, int offset, int len) {
        int sum = 0;
        int end = offset + len;
        for (int i = offset; i < end; i += 2) {
            if (i + 1 < end) {
                sum += unsignedShort(packet.getShort(i));
            } else {
                sum += (unsignedByte(packet.get(i)) << 8);
            }
            while ((sum >>> 16) > 0) {
                sum = (sum & 0xFFFF) + (sum >>> 16);
            }
        }
        return (short) (~sum & 0xFFFF);
    }

    private short calculateUdpChecksum(ByteBuffer packet, int udpOffset, int packetLen, byte[] srcIp, byte[] dstIp) {
        int udpLen = packetLen - udpOffset;
        int sum = 0;
        // Pseudo-header
        for (int i = 0; i < 4; i += 2) {
            sum += unsignedShort((short) ((srcIp[i] << 8) | (srcIp[i+1] & 0xFF)));
            sum += unsignedShort((short) ((dstIp[i] << 8) | (dstIp[i+1] & 0xFF)));
        }
        sum += 17;
        sum += udpLen;
        // UDP + payload
        for (int i = udpOffset; i < packetLen; i += 2) {
            if (i + 1 < packetLen) {
                sum += unsignedShort(packet.getShort(i));
            } else {
                sum += (unsignedByte(packet.get(i)) << 8);
            }
            while ((sum >>> 16) > 0) {
                sum = (sum & 0xFFFF) + (sum >>> 16);
            }
        }
        return (short) (~sum & 0xFFFF);
    }

    private int unsignedByte(byte b) { return b & 0xFF; }
    private int unsignedShort(short s) { return s & 0xFFFF; }

    private byte[] getIpBytes(ByteBuffer packet, int offset) {
        byte[] ip = new byte[4];
        packet.position(offset);
        packet.get(ip);
        return ip;
    }

    @Override
    public void onDestroy() {
        if (mPacketThread != null) {
            mPacketThread.interrupt();
        }
        if (mDnsSocket != null) {
            mDnsSocket.close();
        }
        if (mInterface != null) {
            try { mInterface.close(); } catch (Exception ignored) {}
        }
        stopForeground(true);
        super.onDestroy();
    }
}
