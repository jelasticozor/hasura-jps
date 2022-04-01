namespace HasuraFunction;

using System;
using Newtonsoft.Json;

public record SetPasswordInput(
    [property: JsonProperty("changePasswordId")] string ChangePasswordId,
    [property: JsonProperty("password")] string Password);