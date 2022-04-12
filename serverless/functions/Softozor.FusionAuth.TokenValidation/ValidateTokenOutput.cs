namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record ValidateTokenOutput([property: JsonPropertyName("success")] bool Success);