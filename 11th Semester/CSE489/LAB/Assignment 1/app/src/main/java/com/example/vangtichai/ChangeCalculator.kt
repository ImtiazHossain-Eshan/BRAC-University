package com.example.vangtichai

object ChangeCalculator {
    val DENOMINATIONS = intArrayOf(500, 100, 50, 20, 10, 5, 2, 1)
    fun changeFor(amount: Long): LongArray {
        var remaining = if (amount < 0) 0L else amount
        val counts = LongArray(DENOMINATIONS.size)
        for (i in DENOMINATIONS.indices) {
            val note = DENOMINATIONS[i]
            counts[i] = remaining / note
            remaining %= note
        }
        return counts
    }
}