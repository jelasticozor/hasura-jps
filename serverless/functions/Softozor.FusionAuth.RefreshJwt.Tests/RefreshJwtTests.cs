namespace Softozor.FusionAuth.RefreshJwt.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using io.fusionauth;
using io.fusionauth.domain;
using io.fusionauth.domain.api;
using io.fusionauth.domain.api.jwt;
using io.fusionauth.domain.jwt;
using io.fusionauth.domain.oauth2;
using Moq;
using Softozor.HasuraHandling;
using Xunit;

public class RefreshJwtTests
{
    private const string ValidAccessToken = "valid-access-token";

    private const string InvalidAccessToken = "invalid-access-token";

    private readonly RefreshJwtInput invalidInput = new RefreshJwtInput("invalid-refresh-token");

    private readonly RefreshJwtHandler sut;

    private readonly RefreshJwtInput validInput = new RefreshJwtInput("valid-refresh-token");

    private const string NewRefreshToken = "new-refresh-token";

    private const string NewAccessToken = "new-access-token";

    public RefreshJwtTests()
    {
        this.validInput.Should().NotBe(this.invalidInput);

        var authClient = this.CreateFusionAuthClientStub();
        var mapper = CreateMapper();
        this.sut = new RefreshJwtHandler(authClient, mapper);
    }

    [Fact]
    public async Task WhenHandleWithValidAccessAndRefreshTokensItShouldReturnNewAccessAndRefreshTokens()
    {
        // Arrange

        // Act
        var actualOutput = await this.sut.Handle(this.validInput, ValidAccessToken);

        // Assert
        actualOutput.Token.Should().Be(NewAccessToken);
        actualOutput.RefreshToken.Should().Be(NewRefreshToken);
    }

    [Fact]
    public async Task WhenHandleWithInvalidAccessAndRefreshTokensItShouldThrow()
    {
        // Arrange

        // Act
        Func<Task> act = async () => await this.sut.Handle(this.invalidInput, InvalidAccessToken);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(400);
    }

    private static RefreshRequest RefreshRequestIs(RefreshJwtInput input, string accessToken)
    {
        return Match.Create<RefreshRequest>(
            rq => rq.refreshToken == input.RefreshToken && rq.token == accessToken);
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

        stub.Setup(client => client.ExchangeRefreshTokenForJWTAsync(RefreshRequestIs(this.validInput, ValidAccessToken)))
            .ReturnsAsync(
                new ClientResponse<JWTRefreshResponse>
                {
                    statusCode = 200,
                    successResponse = new JWTRefreshResponse
                    {
                        refreshToken = NewRefreshToken, token = NewAccessToken
                    }
                });

        stub.Setup(client => client.ExchangeRefreshTokenForJWTAsync(RefreshRequestIs(this.invalidInput, InvalidAccessToken)))
            .ReturnsAsync(
                new ClientResponse<JWTRefreshResponse>
                {
                    statusCode = 400,
                    exception = new Exception("the provided refresh token is either expired, was not found, or has been revoked.")
                });

        return stub.Object;
    }
}