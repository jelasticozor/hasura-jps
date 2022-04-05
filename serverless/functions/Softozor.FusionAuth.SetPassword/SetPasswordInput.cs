namespace HasuraFunction;

using System.Text.Json.Serialization;

public record SetPasswordInput(
    [property: JsonPropertyName("change_password_id")] string ChangePasswordId,
    [property: JsonPropertyName("password")] string Password);