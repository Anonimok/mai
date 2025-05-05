package com.example.geradorgrade.model

import com.squareup.moshi.Json

/**
 * Data class representing the response from the /api/session endpoint.
 */
data class SessionResponse(
    @Json(name = "session_id")
    val sessionId: String
)

