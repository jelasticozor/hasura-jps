namespace Softozor.FusionAuth.SignUp.Tests;

using System;
using System.Collections.Generic;
using System.Linq;
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
    private readonly SignUpInput validInput = new SignUpInput(
        new MailAddress("valid-user@example.com"),
        new List<string>{"valid-user-role"},
        Guid.Parse("b7b4b5dc-587f-48fd-bd02-ea395cd98b1e"));

    private readonly SignUpInput invalidInput = new SignUpInput(
        new MailAddress("invalid-user@example.com"),
        new List<string>{"invalid-user-role"},
        Guid.Parse("26ba7627-9384-4b88-becc-1b12ef5bc9db"));

    private readonly Guid userId = Guid.Parse("6c7554ca-6212-439f-b00d-d623013bae03");

    private readonly SignUpHandler sut;

    public SignUpTests()
    {
        var authClient = this.CreateFusionAuthClientStub();
        var mapper = CreateMapper();
        this.sut = new SignUpHandler(authClient, mapper);
    }

    [Fact]
    public async Task WhenHandleWithValidDataItShouldReturnSuccessOutput()
    {
        // Arrange

        // Act
        var actualOutput = await this.sut.Handle(this.validInput);

        // Assert
        actualOutput.UserId.Should().Be(this.userId);
    }

    [Fact]
    public async Task WhenHandleWithInvalidDataItShouldThrow()
    {
        // Arrange

        // Act
        Func<Task> act = async () => await this.sut.Handle(this.invalidInput);

        // Assert
        var actualException = await act.Should().ThrowAsync<HasuraFunctionException>();
        actualException.Which.ErrorCode.Should().Be(400);
    }

    private IFusionAuthAsyncClient CreateFusionAuthClientStub()
    {
        var stub = new Mock<IFusionAuthAsyncClient>();

        stub.Setup(
                client => client.RegisterAsync(
                    null,
                    RegistrationRequestIs(this.validInput)))
            .ReturnsAsync(new ClientResponse<RegistrationResponse>
            {
                statusCode = 200, successResponse = new RegistrationResponse { user = new User { id = this.userId } }
            });

        stub.Setup(
                client => client.RegisterAsync(
                    null,
                    RegistrationRequestIs(this.invalidInput)))
            .ReturnsAsync(new ClientResponse<RegistrationResponse>
            {
                statusCode = 400, exception = new Exception("bad request")
            });

        return stub.Object;
    }

    private static RegistrationRequest RegistrationRequestIs(SignUpInput input)
    {
        return Match.Create<RegistrationRequest>(rq => rq.user.email == input.Email.Address &&
               rq.registration.applicationId == input.AppId && rq.registration.roles.Count == 1 &&
               rq.registration.roles.SequenceEqual(input.Roles) && rq.sendSetPasswordEmail == true);
    }

    private static IMapper CreateMapper()
    {
        var config = new MapperConfiguration(cfg => { cfg.AddProfile<MapperProfile>(); });
        config.AssertConfigurationIsValid();
        return config.CreateMapper();
    }
}