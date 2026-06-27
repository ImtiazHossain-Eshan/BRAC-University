VangtiChai

==========

CSE 489: Mobile Application Development - Assignment 1

A small Android app that lets you type a money amount on a numeric keypad built
from scratch (no system keyboard) and shows the change for that amount in Taka
notes: 500, 100, 50, 20, 10, 5, 2, 1.


Language / build
----------------
- Language : Kotlin
- Min SDK  : 21 (Android 5.0 Lollipop)
- Target / Compile SDK : 36
- Build    : Gradle (wrapper included) + Android Gradle Plugin 9.0.1

Build from the command line:
    gradlew.bat assembleDebug          (build the debug APK)
    gradlew.bat test                   (run the JVM unit tests)
    gradlew.bat installDebug           (install on a running emulator/device)

Or open the folder in Android Studio and press Run.


How it works
------------
- Tapping a digit appends it to the current amount from the right
  (2 -> 23 -> 234). A lone leading 0 is replaced by the next digit, and input
  is capped at 9 digits.
- CLEAR resets the amount to empty.
- The change is computed with a greedy algorithm (largest note first) in
  ChangeCalculator.kt, which is covered by JVM unit tests
  (ChangeCalculatorTest.kt) using the values from the assignment screenshots
  (6, 68, 688, 6880).
- On rotation the activity is recreated; the entered amount is preserved with
  onSaveInstanceState()/savedInstanceState and the change list is recomputed,
  so no state is lost.


Layouts (4 alternatives)
------------------------
The same Activity drives four layouts; each exposes the same view ids, so the
code is layout-independent. No sizes/paddings/margins are hardcoded in the XML;
every dimension lives in a sizes.xml and is selected by resource qualifiers:

  res/layout/activity_main.xml               Phone  portrait  (1-col notes, 3-col keypad)
  res/layout-land/activity_main.xml          Phone  landscape (2-col notes, 4-col keypad)
  res/layout-sw720dp/activity_main.xml       Tablet portrait  (1-col notes, 3-col keypad)
  res/layout-sw720dp-land/activity_main.xml  Tablet landscape (2-col notes, 4-col keypad)

  res/values/sizes.xml                Phone  portrait dimensions
  res/values-land/sizes.xml           Phone  landscape dimensions
  res/values-sw720dp/sizes.xml        Tablet portrait dimensions
  res/values-sw720dp-land/sizes.xml   Tablet landscape dimensions

The screen is split with a ConstraintLayout vertical Guideline: the change
table sits on the left, the keypad on the right. Both the keypad and the
two-column note table use GridLayout so the CLEAR button can span two columns.


Devices / screens tested
------------------------
- Pixel XL phone   (411 x 731 dp)  - portrait and landscape
- Nexus 10 tablet  (800 x 1280 dp) - portrait and landscape
Also sanity-checked on a couple of other emulator profiles (a generic Pixel
phone and a 7" WSVGA tablet) to confirm the layouts scale reasonably.
