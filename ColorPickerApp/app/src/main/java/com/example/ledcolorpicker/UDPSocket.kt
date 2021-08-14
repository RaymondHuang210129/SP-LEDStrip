package com.example.ledcolorpicker

import android.os.Handler
import java.io.IOException
import java.net.DatagramPacket
import java.net.DatagramSocket
import java.net.InetAddress
import java.net.UnknownHostException
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors

class UDPSocket (private val handler: Handler) {
    private val TAG = "UDPSocket"

    private var mThreadPool: ExecutorService? = null
    private var socket: DatagramSocket? = null
    private var receivePacket: DatagramPacket? = null
    private val BUFFER_LENGTH = 1024
    private val receiveByte = ByteArray(BUFFER_LENGTH)

    private var isThreadRunning = false
    private lateinit var clientThread: Thread

    init {
        val cpuNumbers = Runtime.getRuntime().availableProcessors()
        mThreadPool = Executors.newFixedThreadPool(cpuNumbers * 5)
    }

    fun sendMessage(message: String, ipAddress: String, port: Int) {
        mThreadPool?.execute {
            try {
                val targetAddress = InetAddress.getByName(ipAddress)
                val packet = DatagramPacket(message.toByteArray(), message.length, targetAddress, port)
                socket?.send(packet)
            } catch (e: UnknownHostException) {
                e.printStackTrace()
            } catch (e: IOException) {
                e.printStackTrace()
            }
        }
    }
}