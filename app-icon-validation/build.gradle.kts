plugins {
    id("com.android.library")
}

android {
    namespace = "com.royal.design.appiconvalidation"
    compileSdk = 35

    defaultConfig {
        // V10-V15 use VectorDrawable gradients, supported from API 24.
        // Android 8 / API 26 devices are fully within this range.
        minSdk = 24
    }

    flavorDimensions += "appCollection"

    productFlavors {
        create("almalaki") { dimension = "appCollection" }
        create("royalTv") { dimension = "appCollection" }
        create("royalPlus") { dimension = "appCollection" }
        create("rsTv") { dimension = "appCollection" }
        create("ramiDeveloper") { dimension = "appCollection" }
        create("royalAudio") { dimension = "appCollection" }
    }

    sourceSets {
        getByName("almalaki") {
            res.srcDirs("build/generated/royal-app-icons/almalaki/res")
        }
        getByName("royalTv") {
            res.srcDirs("build/generated/royal-app-icons/royal_tv/res")
        }
        getByName("royalPlus") {
            res.srcDirs("build/generated/royal-app-icons/royal_plus/res")
        }
        getByName("rsTv") {
            res.srcDirs("build/generated/royal-app-icons/rs_tv/res")
        }
        getByName("ramiDeveloper") {
            res.srcDirs("build/generated/royal-app-icons/rami_developer/res")
        }
        getByName("royalAudio") {
            res.srcDirs("build/generated/royal-app-icons/royal_audio/res")
        }
    }
}
