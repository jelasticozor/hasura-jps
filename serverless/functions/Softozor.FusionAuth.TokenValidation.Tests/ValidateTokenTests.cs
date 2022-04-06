namespace Softozor.FusionAuth.TokenValidation.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using io.fusionauth;
using io.fusionauth.domain.api.jwt;
using io.fusionauth.jwt.domain;
using Microsoft.Extensions.Logging;
using Moq;
using Softozor.HasuraHandling;
using Xunit;

public class ValidateTokenTests
{
    private const string HasuraClaimsNamespace = "https://hasura.io/jwt/claims";

    private readonly IFusionAuthAsyncClient authClient;

    private readonly ValidateTokenHandler sut;

    public ValidateTokenTests()
    {
        this.authClient = Mock.Of<IFusionAuthAsyncClient>();
        var logger = Mock.Of<ILogger<ValidateTokenHandler>>();
        var mapper = CreateMapper();
        this.sut = new ValidateTokenHandler(this.authClient, logger, mapper);
    }

    [Fact]
    public async Task ShouldThrowErrorUponFailure()
    {
        // Arrange
        const int expectedStatusCode = 400;
        var expectedException = Mock.Of<Exception>();
        var clientResponseStub = new ClientResponse<ValidateResponse>
        {
            statusCode = expectedStatusCode, exception = expectedException
        };
        clientResponseStub.WasSuccessful().Should().BeFalse();
        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.ValidateJWTAsync(It.IsAny<string>())).ReturnsAsync(clientResponseStub);

        // Act
        const string token = "my-invalid-token";
        var input = new BearerTokenAuthorizationHeader(token);
        Func<Task> act = async () => await this.sut.Handle(input);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(expectedStatusCode);
        actualException.Which.InnerException.Should().Be(expectedException);
    }

    [Fact]
    public async Task ShouldReturnUserIdUponSuccess()
    {
        // Arrange
        Environment.SetEnvironmentVariable("HASURA_CLAIMS_NAMESPACE", HasuraClaimsNamespace);
        var userId = Guid.NewGuid();
        var successResponseStub = new ValidateResponse { jwt = CreateJwt(userId) };
        var clientResponseStub = new ClientResponse<ValidateResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };
        clientResponseStub.WasSuccessful().Should().BeTrue();
        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.ValidateJWTAsync(It.IsAny<string>())).ReturnsAsync(clientResponseStub);

        // Act
        const string token = "my-valid-token";
        var input = new BearerTokenAuthorizationHeader(token);
        var actualOutput = await this.sut.Handle(input);

        // Assert
        var expectedOutput = new ValidateTokenOutput(userId);
        actualOutput.Should().BeEquivalentTo(expectedOutput);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        return config.CreateMapper();
    }

    private static JWT CreateJwt(Guid userId)
    {
        var jwt = new JWT
        {
            aud = Guid.NewGuid().ToString(),
            exp = DateTimeOffset.FromUnixTimeSeconds(1591432060),
            iat = DateTimeOffset.FromUnixTimeSeconds(1591428460),
            iss = "company.com",
            sub = Guid.NewGuid().ToString(),
            [HasuraClaimsNamespace] =
                "{\"x-hasura-allowed-roles\": [\"rex\"], \"x-hasura-default-role\": \"rex\", \"x-hasura-user-id\": \"" +
                userId + "\"}"
        };

        return jwt;
    }
}