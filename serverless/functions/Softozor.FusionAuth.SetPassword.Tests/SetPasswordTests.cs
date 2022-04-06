namespace Softozor.FusionAuth.SetPassword.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using io.fusionauth;
using io.fusionauth.domain.api.user;
using Microsoft.Extensions.Logging;
using Moq;
using Softozor.HasuraHandling;
using Xunit;

public class SetPasswordTests
{
    private readonly IFusionAuthAsyncClient authClient;

    private readonly SetPasswordHandler sut;

    public SetPasswordTests()
    {
        this.authClient = Mock.Of<IFusionAuthAsyncClient>();
        var logger = Mock.Of<ILogger<SetPasswordHandler>>();
        var mapper = CreateMapper();
        this.sut = new SetPasswordHandler(this.authClient, logger, mapper);
    }

    [Fact]
    public async Task ShouldUseChangePasswordIdAndPassword()
    {
        // Arrange
        var successResponseStub = new ChangePasswordResponse();
        var clientResponseStub = new ClientResponse<ChangePasswordResponse>
        {
            statusCode = 200, successResponse = successResponseStub
        };

        var authClientMock = Mock.Get(this.authClient);
        authClientMock
            .Setup(client => client.ChangePasswordAsync(It.IsAny<string>(), It.IsAny<ChangePasswordRequest>()))
            .ReturnsAsync(clientResponseStub);

        const string expectedChangePasswordId = "change-password-id";
        const string expectedPassword = "password";
        var validInput = new SetPasswordInput(expectedChangePasswordId, expectedPassword);

        // Act
        await this.sut.Handle(validInput);

        // Assert
        authClientMock.Verify(
            client => client.ChangePasswordAsync(
                expectedChangePasswordId,
                It.Is<ChangePasswordRequest>(r => r.password == expectedPassword)));
    }

    [Theory]
    [InlineData(400)]
    [InlineData(401)]
    public async Task ShouldThrowExceptionWithStatusCodeUponFailure(int expectedStatusCode)
    {
        // Arrange
        var expectedException = Mock.Of<Exception>();
        var clientResponseStub = new ClientResponse<ChangePasswordResponse>
        {
            statusCode = expectedStatusCode, exception = expectedException
        };
        clientResponseStub.WasSuccessful().Should().BeFalse();

        var authClientStub = Mock.Get(this.authClient);
        authClientStub
            .Setup(client => client.ChangePasswordAsync(It.IsAny<string>(), It.IsAny<ChangePasswordRequest>()))
            .ReturnsAsync(clientResponseStub);

        var input = new SetPasswordInput("change-password-id", "password");

        // Act
        Func<Task> act = async () => await this.sut.Handle(input);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(expectedStatusCode);
        actualException.Which.InnerException.Should().Be(expectedException);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        return config.CreateMapper();
    }
}