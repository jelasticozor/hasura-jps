namespace HasuraFunction;

using System.Text.Json.Serialization;

public record RefreshJwtInput([property: JsonPropertyName("refresh_token")] string RefreshToken);