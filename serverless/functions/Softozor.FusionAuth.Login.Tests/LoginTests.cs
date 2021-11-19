namespace Softozor.FusionAuth.Login.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using io.fusionauth;
using io.fusionauth.domain;
using io.fusionauth.domain.api;
using Microsoft.AspNetCore.DataProtection;
using Microsoft.Extensions.Logging;
using Moq;
using Softozor.HasuraHandling.Exceptions;
using Softozor.HasuraHandling.Interfaces;
using Xunit;

public class LoginTests
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly IDataProtector dataProtector;

    private readonly IActionHandler<LoginInput, (LoginOutput, string)> sut;

    private readonly LoginInput validInput = new LoginInput("username", "password", Guid.NewGuid());

    public LoginTests()
    {
        this.authClient = Mock.Of<IFusionAuthAsyncClient>();
        this.dataProtector = Mock.Of<IDataProtector>();
        var logger = Mock.Of<ILogger<LoginHandler>>();
        var mapper = CreateMapper();
        this.sut = new LoginHandler(this.dataProtector, this.authClient, logger, mapper);
    }

    [Theory]
    [InlineData(400)]
    [InlineData(401)]
    public async Task ShouldThrowExceptionWithStatusCodeUponFailure(int expectedStatusCode)
    {
        // Arrange
        var expectedException = Mock.Of<Exception>();
        var clientResponseStub = new ClientResponse<LoginResponse>
        {
            statusCode = expectedStatusCode, exception = expectedException
        };
        clientResponseStub.WasSuccessful().Should().BeFalse();

        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.LoginAsync(It.IsAny<LoginRequest>())).ReturnsAsync(clientResponseStub);

        // Act
        Func<Task> act = async () => await this.sut.Handle(this.validInput);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(expectedStatusCode);
        actualException.Which.InnerException.Should().Be(expectedException);
    }

    [Fact]
    public async Task ShouldReturnLoginCredentialsUponSuccess()
    {
        // Arrange
        const string expectedRefreshToken = "refresh-token";
        const string expectedToken = "token";
        var expectedUserId = Guid.NewGuid();
        var successResponseStub = new LoginResponse
        {
            refreshToken = expectedRefreshToken, token = expectedToken, user = new User { id = expectedUserId }
        };
        var clientResponseStub = new ClientResponse<LoginResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };
        clientResponseStub.WasSuccessful().Should().BeTrue();

        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.LoginAsync(It.IsAny<LoginRequest>())).ReturnsAsync(clientResponseStub);

        // Act
        var (actualLoginOutput, _) = await this.sut.Handle(this.validInput);

        // Assert
        var expectedLoginOutput = new LoginOutput(expectedToken, expectedUserId);
        actualLoginOutput.Should().BeEquivalentTo(expectedLoginOutput);
    }

    [Fact]
    public async Task ShouldReturnProtectedRefreshTokenInCookieUponSuccess()
    {
        // Arrange
        const string expectedRefreshToken = "refresh-token";
        const string expectedToken = "token";
        var expectedUserId = Guid.NewGuid();
        var successResponseStub = new LoginResponse
        {
            refreshToken = expectedRefreshToken, token = expectedToken, user = new User { id = expectedUserId }
        };
        var clientResponseStub = new ClientResponse<LoginResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };
        var dataProtectorMock = Mock.Get(this.dataProtector);
        dataProtectorMock.Setup(protector => protector.Protect(It.IsAny<byte[]>())).Returns<byte[]>(token => token);
        clientResponseStub.WasSuccessful().Should().BeTrue();

        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.LoginAsync(It.IsAny<LoginRequest>())).ReturnsAsync(clientResponseStub);

        // Act
        var (_, actualProtectedRefreshToken) = await this.sut.Handle(this.validInput);

        // Assert
        var expectedProtectedRefreshToken = this.dataProtector.Protect(expectedRefreshToken);
        actualProtectedRefreshToken.Should().NotBe(expectedRefreshToken).And.Be(expectedProtectedRefreshToken);
    }

    [Fact]
    public async Task ShouldThrowWhenRefreshTokenIsNull()
    {
        // Arrange
        var successResponseStub = new LoginResponse
        {
            refreshToken = null, token = "token", user = new User { id = Guid.NewGuid() }
        };
        var clientResponseStub = new ClientResponse<LoginResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };
        clientResponseStub.WasSuccessful().Should().BeTrue();

        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.LoginAsync(It.IsAny<LoginRequest>())).ReturnsAsync(clientResponseStub);

        // Act
        Func<Task> act = async () => await this.sut.Handle(this.validInput);

        // Assert
        var exception = await act.Should().ThrowAsync<HasuraFunctionException>();
        exception.Which.ErrorCode.Should().Be(401);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<LoginProfile>(); });
        return config.CreateMapper();
    }
}