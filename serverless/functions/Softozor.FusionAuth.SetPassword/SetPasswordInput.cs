namespace HasuraFunction;

using System.Text.Json.Serialization;

public record SetPasswordInput(
    [property: JsonPropertyName("changePasswordId")] string ChangePasswordId,
    [property: JsonPropertyName("password")] string Password);