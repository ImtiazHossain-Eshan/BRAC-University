package com.example.assignment2.broadcast

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class CustomBroadcastReceiver(
    private val onMessage: (String) -> Unit
) : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == ACTION_CUSTOM_BROADCAST) {
            val message = intent.getStringExtra(EXTRA_BROADCAST_MESSAGE).orEmpty()
            onMessage(message)
        }
    }

    companion object {
        const val ACTION_CUSTOM_BROADCAST = "com.example.assignment2.action.CUSTOM_BROADCAST"
        const val EXTRA_BROADCAST_MESSAGE = "com.example.assignment2.extra.MESSAGE"
    }
}
