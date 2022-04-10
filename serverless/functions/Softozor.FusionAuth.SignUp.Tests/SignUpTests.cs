namespace Softozor.FusionAuth.SignUp.Tests;

using System;
using System.Net.Mail;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using io.fusionauth;
using io.fusionauth.domain;
using io.fusionauth.domain.api.user;
using Moq;
using Softozor.HasuraHandling;
using Xunit;

public class SignUpTests
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly SignUpHandler sut;

    public SignUpTests()
    {
        this.authClient = Mock.Of<IFusionAuthAsyncClient>();
        var mapper = CreateMapper();
        this.sut = new SignUpHandler(this.authClient, mapper);
    }

    [Fact]
    public async Task ShouldRegisterUserOnApplicationWithProvidedAppId()
    {
        // Arrange
        var successResponseStub = new RegistrationResponse { token = "the-access-token" };
        var clientResponseStub = new ClientResponse<RegistrationResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };

        var authClientMock = Mock.Get(this.authClient);
        authClientMock.Setup(client => client.RegisterAsync(null, It.IsAny<RegistrationRequest>()))
            .ReturnsAsync(clientResponseStub);

        var email = new MailAddress("user@example.com");
        var expectedAppId = Guid.NewGuid();
        var validInput = new SignUpInput(email, "user-role", expectedAppId);

        // Act
        await this.sut.Handle(validInput);

        // Assert
        authClientMock.Verify(
            client => client.RegisterAsync(
                null,
                It.Is<RegistrationRequest>(r => r.registration.applicationId == expectedAppId)),
            Times.Once);
    }

    [Fact]
    public async Task ShouldRegisterUserWithProvidedRole()
    {
        // Arrange
        var successResponseStub = new RegistrationResponse { token = "the-access-token" };
        var clientResponseStub = new ClientResponse<RegistrationResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };

        var authClientMock = Mock.Get(this.authClient);
        authClientMock.Setup(client => client.RegisterAsync(null, It.IsAny<RegistrationRequest>()))
            .ReturnsAsync(clientResponseStub);

        var email = new MailAddress("user@example.com");
        const string expectedRole = "expected-role";
        var validInput = new SignUpInput(email, expectedRole, Guid.NewGuid());

        // Act
        await this.sut.Handle(validInput);

        // Assert
        authClientMock.Verify(
            client => client.RegisterAsync(
                null,
                It.Is<RegistrationRequest>(
                    r => r.registration.roles.Count == 1 && r.registration.roles.Contains(expectedRole))),
            Times.Once);
    }

    [Fact]
    public async Task ShouldRegisterUserWithProvidedEmail()
    {
        // Arrange
        var successResponseStub = new RegistrationResponse { token = "the-access-token" };
        var clientResponseStub = new ClientResponse<RegistrationResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };

        var authClientMock = Mock.Get(this.authClient);
        authClientMock.Setup(client => client.RegisterAsync(null, It.IsAny<RegistrationRequest>()))
            .ReturnsAsync(clientResponseStub);

        const string expectedEmail = "expected-user@example.com";
        var email = new MailAddress(expectedEmail);
        var validInput = new SignUpInput(email, "user-role", Guid.NewGuid());

        // Act
        await this.sut.Handle(validInput);

        // Assert
        authClientMock.Verify(
            client => client.RegisterAsync(null, It.Is<RegistrationRequest>(r => r.user.email == expectedEmail)),
            Times.Once);
    }

    [Fact]
    public async Task ShouldSendSetPasswordEmail()
    {
        // Arrange
        var successResponseStub = new RegistrationResponse { token = "the-access-token" };
        var clientResponseStub = new ClientResponse<RegistrationResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };

        var authClientMock = Mock.Get(this.authClient);
        authClientMock.Setup(client => client.RegisterAsync(null, It.IsAny<RegistrationRequest>()))
            .ReturnsAsync(clientResponseStub);

        var email = new MailAddress("user@example.com");
        var validInput = new SignUpInput(email, "user-role", Guid.NewGuid());

        // Act
        await this.sut.Handle(validInput);

        // Assert
        authClientMock.Verify(
            client => client.RegisterAsync(null, It.Is<RegistrationRequest>(r => r.sendSetPasswordEmail == true)),
            Times.Once);
    }

    [Theory]
    [InlineData(400)]
    [InlineData(401)]
    public async Task ShouldThrowExceptionWithStatusCodeUponFailure(int expectedStatusCode)
    {
        // Arrange
        var expectedException = Mock.Of<Exception>();
        var clientResponseStub = new ClientResponse<RegistrationResponse>
        {
            statusCode = expectedStatusCode, exception = expectedException
        };
        clientResponseStub.WasSuccessful().Should().BeFalse();

        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.RegisterAsync(null, It.IsAny<RegistrationRequest>()))
            .ReturnsAsync(clientResponseStub);

        var email = new MailAddress("user@example.com");
        var validInput = new SignUpInput(email, "user-role", Guid.NewGuid());

        // Act
        Func<Task> act = async () => await this.sut.Handle(validInput);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(expectedStatusCode);
        actualException.Which.InnerException.Should().Be(expectedException);
    }

    [Fact]
    public async Task ShouldReturnRegistrationDataUponSuccess()
    {
        // Arrange
        var expectedUserId = Guid.NewGuid();
        var successResponseStub = new RegistrationResponse { user = new User { id = expectedUserId } };
        var clientResponseStub = new ClientResponse<RegistrationResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };
        clientResponseStub.WasSuccessful().Should().BeTrue();

        var authClientStub = Mock.Get(this.authClient);
        authClientStub.Setup(client => client.RegisterAsync(null, It.IsAny<RegistrationRequest>()))
            .ReturnsAsync(clientResponseStub);

        var email = new MailAddress("user@example.com");
        var validInput = new SignUpInput(email, "user-role", Guid.NewGuid());

        // Act
        var actualOutput = await this.sut.Handle(validInput);

        // Assert
        var expectedOutput = new SignUpOutput(expectedUserId);
        actualOutput.Should().BeEquivalentTo(expectedOutput);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        config.AssertConfigurationIsValid();
        return config.CreateMapper();
    }
}