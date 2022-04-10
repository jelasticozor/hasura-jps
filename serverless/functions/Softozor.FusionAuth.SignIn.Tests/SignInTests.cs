namespace Softozor.FusionAuth.SignIn.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using Softozor.FusionAuth.TestDoubles;
using Softozor.HasuraHandling;
using Xunit;

public class SignInTests
{
    private readonly SignInHandler sut;

    public SignInTests()
    {
        var authClient = new FusionAuthAsyncClient();
        var mapper = CreateMapper();
        this.sut = new SignInHandler(authClient, mapper);
    }

    [Fact]
    public async Task WhenSignInWithValidCredentialsItShouldReturnSuccessOutput()
    {
        // Arrange
        var validInput = new SignInInput(
            "valid-username",
            "valid-password",
            Guid.Parse("60926f3c-1d89-46f4-8b5b-bd61408936e4"));

        // Act
        var actualOutput = await this.sut.Handle(validInput);

        // Assert
        actualOutput.Token.Should().Be("the-access-token");
        actualOutput.RefreshToken.Should().Be("the-refresh-token");
        actualOutput.UserId.Should().Be(Guid.Parse("50238f6a-f57b-4a9a-8032-c4d2a39e8936"));
    }

    [Fact]
    public async Task WhenSignInWithInvalidCredentialsItShouldThrow()
    {
        // Arrange
        var validInput = new SignInInput("invalid-username", "invalid-password", Guid.NewGuid());

        // Act
        Func<Task> act = async () => await this.sut.Handle(validInput);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(404);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        config.AssertConfigurationIsValid();
        return config.CreateMapper();
    }
}