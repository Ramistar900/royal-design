plugins {
    id("com.android.library")
}

android {
    namespace = "com.royal.design.iconvalidation"
    compileSdk = 35

    defaultConfig {
        minSdk = 23
    }

    // Each icon release is compiled as its own flavor. This prevents
    // same-named drawables in different releases from colliding.
    flavorDimensions += "iconVersion"

    productFlavors {
        create("v3") { dimension = "iconVersion" }
        create("v4") { dimension = "iconVersion" }
        create("v5") { dimension = "iconVersion" }
        create("v6") { dimension = "iconVersion" }
        create("v7") { dimension = "iconVersion" }
        create("v8") { dimension = "iconVersion" }
        create("v9") { dimension = "iconVersion" }
    }

    sourceSets {
        getByName("v3") {
            res.srcDirs("../icons/v3/android/res")
        }
        getByName("v4") {
            res.srcDirs("../icons/v4/android/res")
        }
        getByName("v5") {
            res.srcDirs("../icons/v5/finance-shopping/android/res")
        }
        getByName("v6") {
            res.srcDirs("../icons/v6/colorful-finance-shopping/android/res")
        }
        getByName("v7") {
            res.srcDirs("../icons/v7/colorful-controls-media/android/res")
        }
        getByName("v8") {
            res.srcDirs("../icons/v8/colorful-media-product-badges/android/res")
        }
        getByName("v9") {
            res.srcDirs("../icons/v9/cafe-orders/android/res")
        }
    }
}
