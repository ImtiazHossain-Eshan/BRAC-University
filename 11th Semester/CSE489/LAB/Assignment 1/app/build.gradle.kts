import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    // Kotlin is compiled via AGP 9.0's built-in Kotlin support.
    id("com.android.application")
}

android {
    namespace = "com.example.vangtichai"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.example.vangtichai"
        minSdk = 21
        // Target 34 to keep the classic opaque action bar with content laid out
        // below it (avoids the API 35+ edge-to-edge enforcement, which would draw
        // the "Taka:" label behind the action bar). minSdk stays at 21.
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

kotlin {
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_17)
    }
}

dependencies {
    implementation("androidx.appcompat:appcompat:1.7.1")
    implementation("androidx.constraintlayout:constraintlayout:2.2.1")
    testImplementation("junit:junit:4.13.2")
}
