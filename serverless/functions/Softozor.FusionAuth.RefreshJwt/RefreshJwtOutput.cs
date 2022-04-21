namespace HasuraFunction;

using System.Text.Json.Serialization;

public record RefreshJwtOutput(
    [property: JsonPropertyName("refresh_token")] string RefreshToken,
    [property: JsonPropertyName("token")] string Token);