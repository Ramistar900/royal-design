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
                "../icons/v5/finance-shopping/android/res",
                "../icons/v6/colorful-finance-shopping/android/res",
                "../icons/v7/colorful-controls-media/android/res",
                "../icons/v8/colorful-media-product-badges/android/res",
                "../icons/v9/cafe-orders/android/res"
            )
        }
    }
}
