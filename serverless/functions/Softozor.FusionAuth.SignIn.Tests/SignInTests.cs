namespace Softozor.FusionAuth.SignIn.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using io.fusionauth;
using io.fusionauth.domain;
using io.fusionauth.domain.api;
using Moq;
using Softozor.HasuraHandling;
using Xunit;

public class SignInTests
{
    private const string AccessToken = "the-access-token";

    private const string RefreshToken = "the-refresh-token";

    private readonly SignInInput invalidInput = new SignInInput("invalid-username", "invalid-password", Guid.NewGuid());

    private readonly SignInHandler sut;

    private readonly Guid userId = Guid.Parse("50238f6a-f57b-4a9a-8032-c4d2a39e8936");

    private readonly SignInInput validInput = new SignInInput(
        "valid-username",
        "valid-password",
        Guid.Parse("60926f3c-1d89-46f4-8b5b-bd61408936e4"));

    public SignInTests()
    {
        this.validInput.Should().NotBe(this.invalidInput);

        var authClient = this.CreateFusionAuthClientStub();
        var mapper = CreateMapper();
        this.sut = new SignInHandler(authClient, mapper);
    }

    [Fact]
    public async Task WhenHandleWithValidCredentialsItShouldReturnSuccessOutput()
    {
        // Arrange

        // Act
        var actualOutput = await this.sut.Handle(this.validInput);

        // Assert
        actualOutput.Token.Should().Be(AccessToken);
        actualOutput.RefreshToken.Should().Be(RefreshToken);
        actualOutput.UserId.Should().Be(this.userId);
    }

    [Fact]
    public async Task WhenHandleWithInvalidCredentialsItShouldThrow()
    {
        // Arrange

        // Act
        Func<Task> act = async () => await this.sut.Handle(this.invalidInput);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(404);
    }

    private static LoginRequest LoginRequestIs(SignInInput input)
    {
        return Match.Create<LoginRequest>(
            rq => rq.loginId == input.Username && rq.password == input.Password && rq.applicationId == input.AppId);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        config.AssertConfigurationIsValid();
        return config.CreateMapper();
    }

    private IFusionAuthAsyncClient CreateFusionAuthClientStub()
    {
        var stub = new Mock<IFusionAuthAsyncClient>();

        stub.Setup(client => client.LoginAsync(LoginRequestIs(this.validInput)))
            .ReturnsAsync(
                new ClientResponse<LoginResponse>
                {
                    statusCode = 200,
                    successResponse = new LoginResponse
                    {
                        refreshToken = RefreshToken, token = AccessToken, user = new User { id = this.userId }
                    }
                });

        stub.Setup(client => client.LoginAsync(LoginRequestIs(this.invalidInput)))
            .ReturnsAsync(
                new ClientResponse<LoginResponse>
                {
                    statusCode = 404,
                    exception = new Exception("the user was not found or the password was incorrect.")
                });

        return stub.Object;
    }
}