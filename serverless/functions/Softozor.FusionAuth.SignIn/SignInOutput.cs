namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record SignInOutput(
    [property: JsonPropertyName("refresh_token")] string RefreshToken,
    [property: JsonPropertyName("token")] string Token,
    [property: JsonPropertyName("user_id")] Guid UserId);