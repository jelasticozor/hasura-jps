namespace Softozor.FusionAuth.SignUp.Tests;

using System;
using System.Diagnostics.CodeAnalysis;
using System.Net.Mail;
using System.Text.Json;
using System.Text.Json.Serialization;
using FluentAssertions;
using HasuraFunction;
using Softozor.HasuraHandling.Exceptions;
using Xunit;

public class EmailConverterTests
{
    [Fact]
    public void ShouldConvertValidEmailToMailAddress()
    {
        // Arrange
        const string expectedEmail = "valid@example.com";
        var jsonData = @"{""email"": """ + expectedEmail + @"""}";

        // Act
        var actual = JsonSerializer.Deserialize<JsonData>(jsonData);

        // Assert
        actual.Should().NotBeNull();
        actual!.Email.Address.Should().Be(expectedEmail);
    }

    [Fact]
    public void ShouldThrowWhenProvidedWithInvalidEmail()
    {
        // Arrange
        var jsonData = @"{""email"": ""invalid""}";

        // Act
        Action act = () => JsonSerializer.Deserialize<JsonData>(jsonData);

        // Assert
        act.Should().Throw<HasuraFunctionException>().Where(e => e.ErrorCode == 400);
    }

    [SuppressMessage(
        "Performance",
        "CA1812: Avoid uninstantiated internal classes",
        Justification = "Used as generic argument in deserialization method")]
    internal record JsonData(
        [property: JsonPropertyName("email")] [property: JsonConverter(typeof(EmailConverter))] MailAddress Email);
}