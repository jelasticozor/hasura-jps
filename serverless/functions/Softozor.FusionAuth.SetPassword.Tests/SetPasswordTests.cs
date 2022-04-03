namespace Softozor.FusionAuth.SetPassword.Tests;

using AutoMapper;
using HasuraFunction;
using io.fusionauth;
using Microsoft.Extensions.Logging;
using Moq;

public class SetPasswordTests
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly SetPasswordHandler sut;

    // private readonly SetPasswordInput validInput = new SetPasswordInput("change-password-id", "password");

    public SetPasswordTests()
    {
        this.authClient = Mock.Of<IFusionAuthAsyncClient>();
        var logger = Mock.Of<ILogger<SetPasswordHandler>>();
        var mapper = CreateMapper();
        this.sut = new SetPasswordHandler(this.authClient, logger, mapper);
    }

    /*[Theory]
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
        var expectedLoginOutput = new SetPasswordOutput(expectedToken, expectedUserId);
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
    }*/

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        return config.CreateMapper();
    }
}