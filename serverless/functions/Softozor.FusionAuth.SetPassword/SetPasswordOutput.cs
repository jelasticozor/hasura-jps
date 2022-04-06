namespace HasuraFunction;

using System.Text.Json.Serialization;

public record SetPasswordOutput([property: JsonPropertyName("success")] bool Success);