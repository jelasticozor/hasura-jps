namespace HasuraFunction;

using System;
using System.Net.Mail;
using System.Text.Json.Serialization;

public record SignUpInput(
    [property: JsonPropertyName("email")] [property: JsonConverter(typeof(EmailConverter))] MailAddress Email,
    [property: JsonPropertyName("role")] string Role,
    [property: JsonPropertyName("app_id")] Guid AppId);