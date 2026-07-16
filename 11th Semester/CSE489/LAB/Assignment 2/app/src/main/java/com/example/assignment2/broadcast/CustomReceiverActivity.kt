package com.example.assignment2.broadcast

import android.content.Intent
import android.content.IntentFilter
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.example.assignment2.R
import com.example.assignment2.databinding.ActivityCustomReceiverBinding

class CustomReceiverActivity : AppCompatActivity() {

    private lateinit var binding: ActivityCustomReceiverBinding
    private lateinit var receiver: CustomBroadcastReceiver

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityCustomReceiverBinding.inflate(layoutInflater)
        setContentView(binding.root)
        supportActionBar?.setDisplayHomeAsUpEnabled(true)

        // 1) Create the custom broadcast receiver and register it dynamically.
        receiver = CustomBroadcastReceiver { message ->
            binding.textStatus.text = getString(R.string.received_label)
            binding.textReceived.text = message
        }
        val filter = IntentFilter(CustomBroadcastReceiver.ACTION_CUSTOM_BROADCAST)
        // Registered as NOT_EXPORTED: this is an app-internal broadcast only.
        ContextCompat.registerReceiver(
            this,
            receiver,
            filter,
            ContextCompat.RECEIVER_NOT_EXPORTED
        )

        // 2) Take the message from the second activity and broadcast it to our receiver.
        val message = intent.getStringExtra(EXTRA_MESSAGE).orEmpty()
        val broadcast = Intent(CustomBroadcastReceiver.ACTION_CUSTOM_BROADCAST)
            .setPackage(packageName) // keep the broadcast inside this app
            .putExtra(CustomBroadcastReceiver.EXTRA_BROADCAST_MESSAGE, message)
        sendBroadcast(broadcast)
    }

    override fun onDestroy() {
        super.onDestroy()
        unregisterReceiver(receiver)
    }

    override fun onSupportNavigateUp(): Boolean {
        finish()
        return true
    }

    companion object {
        const val EXTRA_MESSAGE = "com.example.assignment2.extra.INPUT_MESSAGE"
    }
}
