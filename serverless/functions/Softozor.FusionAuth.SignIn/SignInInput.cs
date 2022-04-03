namespace HasuraFunction;

using System;
using System.Text.Json.Serialization;

public record SignInInput(
    [property: JsonPropertyName("username")] string Username,
    [property: JsonPropertyName("password")] string Password,
    [property: JsonPropertyName("appId")] Guid AppId);