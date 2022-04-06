namespace HasuraFunction;

using System;
using System.Net.Mail;
using System.Text.Json;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.Http;
using Softozor.HasuraHandling;

public class EmailConverter : JsonConverter<MailAddress>
{
    public override MailAddress Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        try
        {
            return new MailAddress(reader.GetString()!);
        }
        catch (FormatException ex)
        {
            throw new HasuraFunctionException("Input email is not an email", StatusCodes.Status400BadRequest, ex);
        }
    }

    public override void Write(Utf8JsonWriter writer, MailAddress value, JsonSerializerOptions options)
    {
        throw new NotImplementedException();
    }
}