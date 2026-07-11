plugins {
    alias(libs.plugins.android.application)
    // Kotlin support is built into AGP 9.0+, so no separate Kotlin plugin is applied.
}

android {
    namespace = "com.example.assignment2"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.example.assignment2"
        minSdk = 26
        // Target 34 so the platform does not force Android 15+ edge-to-edge; the classic
        // ActionBar then insets content correctly on every screen. compileSdk stays at 36.
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
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
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }

    // Kotlin's jvmTarget defaults to compileOptions.targetCompatibility (11) with built-in Kotlin.

    buildFeatures {
        viewBinding = true
    }
}

dependencies {
    implementation(libs.androidx.core.ktx)
    implementation(libs.androidx.appcompat)
    implementation(libs.material)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.navigation.fragment.ktx)
    implementation(libs.androidx.navigation.ui.ktx)
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.fragment.ktx)
    implementation(libs.glide)
}
