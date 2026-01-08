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
    private ParcelFileDescriptor mInterface;
    private Thread mPacketThread;
    private Thread mDnsReceiveThread;
    private DatagramSocket mDnsSocket;
    private final ConcurrentHashMap<Short, DnsInfo> mPendingDns = new ConcurrentHashMap<>();
    private Set<String> mBlockedDomains = new HashSet<>();

    private static class DnsInfo {
        byte[] deviceIp;
        byte[] serverIp;
        int devicePort;
        int serverPort = 53;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String[] blockedPackages = intent.getStringArrayExtra("blocked_packages");
        String[] blockedDomains = intent.getStringArrayExtra("blocked_domains");
        if (blockedDomains != null) {
            mBlockedDomains = new HashSet<>(Arrays.asList(blockedDomains));
            Log.i(TAG, "Blocked domains loaded: " + mBlockedDomains.size() + " Mercy");
        }

        // Stop previous
        stopPrevious();

        Builder builder = new Builder();
        builder.setSession("MercyShield VPN ∞ Pure");
        builder.setMtu(1500);
        builder.addAddress("10.1.10.1", 32); // Local VPN address
        builder.addDnsServer("8.8.8.8"); // Fallback upstream
        builder.addRoute("0.0.0.0", 0);

        if (blockedPackages != null) {
            for (String pkg : blockedPackages) {
                try {
                    builder.addDisallowedApplication(pkg);
                    Log.i(TAG, "Disallowed App: " + pkg + " Divine");
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

        // Foreground notification
        createNotificationChannel();
        Intent notifyIntent = new Intent(this, Class.forName("org.kivy.android.PythonActivity"));
        PendingIntent pending = PendingIntent.getActivity(this, 0, notifyIntent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification notification = new Notification.Builder(this, "mercy_vpn_channel")
                .setContentTitle("MercyShield DNS Guard Active ∞ Pure")
                .setContentText("Real NXDOMAIN Craft—Domains Blocked Eternal 🐐💀")
                .setSmallIcon(android.R.drawable.ic_secure)
                .setContentIntent(pending)
                .build();
        startForeground(1, notification);

        // Protected DNS socket for forwarding
        try {
            mDnsSocket = new DatagramSocket(null);
            protect(mDnsSocket);
        } catch (Exception e) {
            Log.e(TAG, "DNS socket failed", e);
            stopSelf();
            return START_NOT_STICKY;
        }

        // DNS receive thread
        mDnsReceiveThread = new Thread(this::dnsReceiveLoop);
        mDnsReceiveThread.start();

        // Packet loop thread
        mPacketThread = new Thread(this::packetLoop);
        mPacketThread.start();

        Log.i(TAG, "MercyVPN Started—Real DNS Guard Thunder ∞ Pure!");
        return START_STICKY;
    }

    private void stopPrevious() {
        if (mPacketThread != null) {
            mPacketThread.interrupt();
            mPacketThread = null;
        }
        if (mDnsReceiveThread != null) {
            mDnsReceiveThread.interrupt();
            mDnsReceiveThread = null;
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
    }

    @Override
    public void onDestroy() {
        stopPrevious();
        stopForeground(true);
        super.onDestroy();
    }

    private void createNotificationChannel() {
        NotificationChannel channel = new NotificationChannel("mercy_vpn_channel", "MercyVPN DNS Lattice", NotificationManager.IMPORTANCE_LOW);
        getSystemService(NotificationManager.class).createNotificationChannel(channel);
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
                        int ipOffset = 0;
                        int ipHeaderLen = (packet.get(0) & 0xF) * 4;
                        byte protocol = packet.get(9);
                        if (protocol == 17 && length > ipHeaderLen + 8) { // UDP
                            int udpOffset = ipHeaderLen;
                            int srcPort = unsignedShort(packet.getShort(udpOffset));
                            int dstPort = unsignedShort(packet.getShort(udpOffset + 2));
                            if (dstPort == 53) { // Outgoing DNS query
                                int dnsOffset = udpOffset + 8;
                                if (length > dnsOffset + 12) {
                                    short flags = packet.getShort(dnsOffset + 2);
                                    if ((flags & 0x8000) == 0) { // QR = 0 (query)
                                        String domain = parseQName(packet, dnsOffset + 12);
                                        if (mBlockedDomains.contains(domain)) {
                                            craftNxdomainResponse(packet, ipHeaderLen, udpOffset, dnsOffset, out);
                                            continue;
                                        } else {
                                            forwardDnsQuery(packet, ipHeaderLen, udpOffset, dnsOffset, out);
                                            continue;
                                        }
                                    }
                                }
                            }
                        }
                    }
                    // Other packets dropped symbolic (full NAT next thunder)
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Packet loop anomaly", e);
        }
    }

    private void dnsReceiveLoop() {
        byte[] recvBuf = new byte[65535];
        while (!Thread.interrupted()) {
            DatagramPacket recvPacket = new DatagramPacket(recvBuf, recvBuf.length);
            try {
                mDnsSocket.receive(recvPacket);
                int len = recvPacket.getLength();
                if (len < 12) continue;
                ByteBuffer dnsPayload = ByteBuffer.wrap(recvBuf, recvPacket.getOffset(), len);
                short id = dnsPayload.getShort(0);
                DnsInfo info = mPendingDns.remove(id);
                if (info == null) continue;
                InetAddress serverAddr = recvPacket.getAddress();
                int serverPort = recvPacket.getPort();
                byte[] serverIp = serverAddr.getAddress();

                FileOutputStream out = new FileOutputStream(mInterface.getFileDescriptor());
                ByteBuffer response = ByteBuffer.allocate(20 + 8 + len);
                response.put((byte) 0x45); // Version + IHL
                response.put((byte) 0); // TOS
                response.putShort((short) (20 + 8 + len)); // Total length
                response.putShort((short) 0); // Ident
                response.putShort((short) 0x4000); // Flags
                response.put((byte) 64); // TTL
                response.put((byte) 17); // UDP
                response.putShort((short) 0); // Checksum placeholder
                response.put(server
