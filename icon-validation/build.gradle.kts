plugins {
    id("com.android.library")
}

android {
    namespace = "com.royal.design.iconvalidation"
    compileSdk = 35

    defaultConfig {
        minSdk = 23
    }

    sourceSets {
        getByName("main") {
            res.srcDirs(
                "../icons/v3/android/res",
                "../icons/v5/finance-shopping/android/res"
            )
        }
    }
}
