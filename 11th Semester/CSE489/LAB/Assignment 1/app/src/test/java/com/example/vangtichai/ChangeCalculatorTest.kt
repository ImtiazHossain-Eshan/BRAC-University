package com.example.vangtichai

import org.junit.Assert.assertArrayEquals
import org.junit.Test

class ChangeCalculatorTest {

    @Test
    fun zeroGivesNoNotes() {
        assertArrayEquals(
            longArrayOf(0, 0, 0, 0, 0, 0, 0, 0),
            ChangeCalculator.changeFor(0)
        )
    }

    @Test
    fun six() {
        assertArrayEquals(
            longArrayOf(0, 0, 0, 0, 0, 1, 0, 1),
            ChangeCalculator.changeFor(6)
        )
    }

    @Test
    fun sixtyEight() { // 68 = 50 + 10 + 5 + 2 + 1
        assertArrayEquals(
            longArrayOf(0, 0, 1, 0, 1, 1, 1, 1),
            ChangeCalculator.changeFor(68)
        )
    }

    @Test
    fun sixEightyEight() { // 688 = 500 + 100 + 50 + 20 + 10 + 5 + 2 + 1
        assertArrayEquals(
            longArrayOf(1, 1, 1, 1, 1, 1, 1, 1),
            ChangeCalculator.changeFor(688)
        )
    }

    @Test
    fun sixThousandEightHundredEighty() {
        assertArrayEquals(
            longArrayOf(13, 3, 1, 1, 1, 0, 0, 0),
            ChangeCalculator.changeFor(6880)
        )
    }

    @Test
    fun negativeTreatedAsZero() {
        assertArrayEquals(
            longArrayOf(0, 0, 0, 0, 0, 0, 0, 0),
            ChangeCalculator.changeFor(-5)
        )
    }
}
