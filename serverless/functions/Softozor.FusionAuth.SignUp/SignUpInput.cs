namespace HasuraFunction;

using System;
using System.Collections.Generic;
using System.Net.Mail;
using System.Text.Json.Serialization;

public record SignUpInput(
    [property: JsonPropertyName("email")] [property: JsonConverter(typeof(EmailConverter))] MailAddress Email,
    [property: JsonPropertyName("roles")] IEnumerable<string> Roles,
    [property: JsonPropertyName("app_id")] Guid AppId);