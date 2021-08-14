package com.example.ledcolorpicker

import android.graphics.drawable.ColorDrawable
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.CheckBox
import android.widget.TextView
import androidx.appcompat.app.ActionBar
import androidx.appcompat.app.AppCompatActivity
import com.github.dhaval2404.colorpicker.ColorPickerView
import java.io.IOException
import java.lang.Exception
import java.net.*


class MainActivity : AppCompatActivity() {

    //layout elements
    private var serverIPAddress: TextView? = null
    private var serverPort: TextView? = null
    private var stripColorPicker: ColorPickerView? = null
    private var numOfLEDs: TextView? = null
    private var sendAllBytes: CheckBox? = null
    private var turnOffButton: Button? = null
    private var rainbowModeButton: Button? = null
    private var manualModeButton: Button? = null
    private var whiteModeButton: Button? = null
    private var IonOnButton: Button? = null
    private var IonOffButton: Button? = null

    private val localPort: Int = 20080


    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        initElements()


        stripColorPicker?.setColorListener { colorInt, colorString ->
            Thread {
                try {
                    val window = window
                    val actionBar: ActionBar? = supportActionBar
                    window.statusBarColor = colorInt
                    actionBar?.setBackgroundDrawable(ColorDrawable(colorInt))
                    var socket: DatagramSocket = DatagramSocket(null)
                    socket.reuseAddress = true
                    socket.bind(InetSocketAddress(localPort))
                    val targetAddress = InetAddress.getByName(serverIPAddress?.getText().toString())
                    if (sendAllBytes?.isChecked!!) {
                        val colorByteBlue: Byte = colorInt.toByte()
                        val colorByteGreen: Byte = colorInt.shr(8).toByte()
                        val colorByteRed: Byte = colorInt.shr(16).toByte()
                        val colorByteArray: ByteArray = ByteArray(numOfLEDs?.text.toString().toInt() * 3)
                        for (i in 0..colorByteArray.lastIndex) {
                            if (i.rem(3) == 0) {
                                colorByteArray[i] = colorByteRed
                            } else if (i.rem(3) == 1) {
                                colorByteArray[i] = colorByteGreen
                            } else {
                                colorByteArray[i] = colorByteBlue
                            }
                        }
                        val packet = DatagramPacket(colorByteArray, colorByteArray.size, targetAddress, serverPort?.getText().toString().toInt())
                        socket.send(packet)
                        socket.close()
                    } else {
                        val packet = DatagramPacket(colorString.toByteArray(), colorString.length, targetAddress, serverPort?.getText().toString().toInt())
                        socket.send(packet)
                        socket.close()
                    }
                } catch (e: UnknownHostException) {
                    e.printStackTrace()
                } catch (e: IOException) {
                    e.printStackTrace()
                } catch (e: Exception) {
                    e.printStackTrace()
                }

            }.start()

        }

        turnOffButton?.setOnClickListener {
            Thread {
                try {
                    val url = URL("http://"+ serverIPAddress?.getText().toString() + ":8699/off")
                    with (url.openConnection() as HttpURLConnection) {
                        requestMethod = "GET"
                        Log.d("Button", "Sent 'GET' request to URL : $url; Response Code : $responseCode")
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }.start()
        }

        rainbowModeButton?.setOnClickListener {
            Thread {
                try {
                    val url = URL("http://"+ serverIPAddress?.getText().toString() + ":8699/rainbow")
                    with (url.openConnection() as HttpURLConnection) {
                        requestMethod = "GET"
                        Log.d("Button", "Sent 'GET' request to URL : $url; Response Code : $responseCode")
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }.start()
        }

        manualModeButton?.setOnClickListener {
            Thread {
                try {
                    val url = URL("http://"+ serverIPAddress?.getText().toString() + ":8699/manual")
                    with (url.openConnection() as HttpURLConnection) {
                        requestMethod = "GET"
                        Log.d("Button", "Sent 'GET' request to URL : $url; Response Code : $responseCode")
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }.start()
        }

        whiteModeButton?.setOnClickListener {
            Thread {
                try {
                    val url = URL("http://" + serverIPAddress?.getText().toString() + ":8699/white")
                    with (url.openConnection() as HttpURLConnection) {
                        requestMethod = "GET"
                        Log.d("Button", "Sent 'GET' request to URL : $url; Response Code : $responseCode")
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }.start()
        }

        IonOnButton?.setOnClickListener {
            Thread {
                try {
                    var url = URL("http://" + serverIPAddress?.getText().toString() + ":8671/on")
                    with (url.openConnection() as HttpURLConnection) {
                        requestMethod = "GET"
                        Log.d("Button", "Sent 'GET' request to URL : $url; Response Code : $responseCode")
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }.start()
        }

        IonOffButton?.setOnClickListener {
            Thread {
                try {
                    var url = URL("http://" + serverIPAddress?.getText().toString() + ":8671/off")
                    with (url.openConnection() as HttpURLConnection) {
                        requestMethod = "GET"
                        Log.d("Button", "Sent 'GET' request to URL : $url; Response Code : $responseCode")
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                }
            }.start()
        }
    }

    private fun initElements() {
        serverIPAddress = findViewById<TextView>(R.id.serverIpAddress)
        serverPort = findViewById<TextView>(R.id.serverPort)
        stripColorPicker = findViewById<ColorPickerView>(R.id.stripColorPicker)
        numOfLEDs = findViewById<TextView>(R.id.numOfBulb)
        sendAllBytes = findViewById<CheckBox>(R.id.sendByteCheckBox)
        whiteModeButton = findViewById<Button>(R.id.whiteModeButton)
        rainbowModeButton = findViewById<Button>(R.id.rainbowModeButton)
        turnOffButton = findViewById<Button>(R.id.turnOffButton)
        manualModeButton = findViewById<Button>(R.id.manualModeButton)
        IonOnButton = findViewById<Button>(R.id.ionOnButton)
        IonOffButton = findViewById<Button>(R.id.ionOffButton)
    }




}