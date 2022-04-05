namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record SignInOutput(
    [property: JsonPropertyName("token")] string Token,
    [property: JsonPropertyName("user_id")] Guid UserId);