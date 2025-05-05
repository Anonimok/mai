package com.example.geradorgrade.model

import com.squareup.moshi.Json

/**
 * Data class representing the request body for the /api/schedule/preferences endpoint.
 */
data class PreferencesRequest(
    @Json(name = "min_credits")
    val minCredits: Int,
    @Json(name = "max_credits")
    val maxCredits: Int
    // Add other preferences here in the future (e.g., interests, time constraints)
)

