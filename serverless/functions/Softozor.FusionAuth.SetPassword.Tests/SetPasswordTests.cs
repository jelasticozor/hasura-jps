namespace Softozor.FusionAuth.SetPassword.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using Microsoft.Extensions.Logging;
using Moq;
using Softozor.FusionAuth.TestDoubles;
using Softozor.HasuraHandling;
using Xunit;

public class SetPasswordTests
{
    private const string ValidPassword = "my-password";

    private readonly SetPasswordHandler sut;

    public SetPasswordTests()
    {
        var authClient = new FusionAuthAsyncClient();
        var logger = Mock.Of<ILogger<SetPasswordHandler>>();
        var mapper = CreateMapper();
        this.sut = new SetPasswordHandler(authClient, logger, mapper);
    }

    [Fact]
    public async Task WhenHandlingValidChangePasswordIdAndNonEmptyPasswordItShouldNotThrow()
    {
        // Arrange
        var validInput = new SetPasswordInput(FusionAuthAsyncClient.SuccessChangePasswordId, ValidPassword);

        // Act
        Func<Task> act = async () => await this.sut.Handle(validInput);

        // Assert
        await act.Should().NotThrowAsync();
    }

    [Theory]
    [InlineData("")]
    [InlineData(" ")]
    public async Task WhenHandlingValidChangePasswordIdAndNoPasswordItShouldThrowBadRequest(
        string emptyOrWhitespacePassword)
    {
        // Arrange
        var input = new SetPasswordInput(FusionAuthAsyncClient.SuccessChangePasswordId, emptyOrWhitespacePassword);

        // Act
        Func<Task> act = async () => await this.sut.Handle(input);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(400);
    }

    [Fact]
    public async Task WhenHandlingInvalidChangePasswordIdAndNonEmptyPasswordItShouldThrowNotFound()
    {
        // Arrange

        var input = new SetPasswordInput("failure-change-password-id", ValidPassword);

        // Act
        Func<Task> act = async () => await this.sut.Handle(input);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(404);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        return config.CreateMapper();
    }
}