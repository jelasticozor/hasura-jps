namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record SignUpOutput([property: JsonPropertyName("userId")] Guid UserId);