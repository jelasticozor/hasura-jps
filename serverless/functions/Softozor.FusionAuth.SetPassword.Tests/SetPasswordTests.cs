namespace Softozor.FusionAuth.SetPassword.Tests;

using System;
using System.Threading.Tasks;
using AutoMapper;
using FluentAssertions;
using HasuraFunction;
using io.fusionauth;
using io.fusionauth.domain.api.user;
using Moq;
using Softozor.HasuraHandling;
using Xunit;

public class SetPasswordTests
{
    private const string SuccessPasswordId = "success-change-password-id";

    private const string FailurePasswordId = "failure-change-password-id";

    private const string ValidPassword = "my-password";

    private readonly SetPasswordHandler sut;

    public SetPasswordTests()
    {
        SuccessPasswordId.Should().NotBe(FailurePasswordId);

        var authClient = CreateFusionAuthClientStub();
        var mapper = CreateMapper();
        this.sut = new SetPasswordHandler(authClient, mapper);
    }

    [Fact]
    public async Task WhenHandleValidChangePasswordIdAndNonEmptyPasswordItShouldNotThrow()
    {
        // Arrange
        var validInput = new SetPasswordInput(SuccessPasswordId, ValidPassword);

        // Act
        Func<Task> act = async () => await this.sut.Handle(validInput);

        // Assert
        await act.Should().NotThrowAsync();
    }

    [Theory]
    [InlineData("")]
    [InlineData(" ")]
    public async Task WhenHandleValidChangePasswordIdAndNoPasswordItShouldThrowBadRequest(
        string emptyOrWhitespacePassword)
    {
        // Arrange
        var input = new SetPasswordInput(SuccessPasswordId, emptyOrWhitespacePassword);

        // Act
        Func<Task> act = async () => await this.sut.Handle(input);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(400);
    }

    [Fact]
    public async Task WhenHandleInvalidChangePasswordIdAndNonEmptyPasswordItShouldThrowNotFound()
    {
        // Arrange
        var input = new SetPasswordInput(FailurePasswordId, ValidPassword);

        // Act
        Func<Task> act = async () => await this.sut.Handle(input);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(404);
    }

    private static IFusionAuthAsyncClient CreateFusionAuthClientStub()
    {
        var stub = new Mock<IFusionAuthAsyncClient>();
        stub.Setup(
                client => client.ChangePasswordAsync(
                    SuccessPasswordId,
                    It.Is<ChangePasswordRequest>(rq => rq.password == ValidPassword)))
            .ReturnsAsync(
                new ClientResponse<ChangePasswordResponse>
                {
                    statusCode = 200, successResponse = new ChangePasswordResponse()
                });

        stub.Setup(
                client => client.ChangePasswordAsync(
                    SuccessPasswordId,
                    It.Is<ChangePasswordRequest>(rq => string.IsNullOrWhiteSpace(rq.password))))
            .ReturnsAsync(
                new ClientResponse<ChangePasswordResponse>
                {
                    statusCode = 400, exception = new Exception("malformed request")
                });

        stub.Setup(
                client => client.ChangePasswordAsync(
                    It.Is<string>(id => id != SuccessPasswordId),
                    It.IsAny<ChangePasswordRequest>()))
            .ReturnsAsync(
                new ClientResponse<ChangePasswordResponse>
                {
                    statusCode = 404, exception = new Exception("could not find user from change password id")
                });

        return stub.Object;
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        config.AssertConfigurationIsValid();
        return config.CreateMapper();
    }
}