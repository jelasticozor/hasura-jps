namespace HasuraFunction;

using System;
using System.Net.Mail;
using System.Text.Json;
using System.Text.Json.Serialization;

public class EmailConverter : JsonConverter<MailAddress>
{
    public override MailAddress Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
    {
        return new MailAddress(reader.GetString()!);
    }

    public override void Write(Utf8JsonWriter writer, MailAddress value, JsonSerializerOptions options)
    {
        throw new NotImplementedException();
    }
}