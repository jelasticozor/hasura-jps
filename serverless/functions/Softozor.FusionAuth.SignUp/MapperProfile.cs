namespace HasuraFunction;

using System.Collections.Generic;
using System.Linq;
using AutoMapper;
using io.fusionauth.domain;
using io.fusionauth.domain.api.user;

public class MapperProfile : Profile
{
    public MapperProfile()
    {
        this.CreateMap<SignUpInput, RegistrationRequest>()
            .ForMember(dest => dest.skipVerification, opt => opt.Ignore())
            .ForMember(dest => dest.disableDomainBlock, opt => opt.Ignore())
            .ForMember(dest => dest.generateAuthenticationToken, opt => opt.Ignore())
            .ForMember(dest => dest.skipRegistrationVerification, opt => opt.Ignore())
            .ForMember(dest => dest.eventInfo, opt => opt.Ignore())
            .ForMember(dest => dest.sendSetPasswordEmail, opt => opt.MapFrom(_ => true))
            .ForMember(dest => dest.user, opt => opt.MapFrom(src => new User { email = src.Email.Address }))
            .ForMember(
                dest => dest.registration,
                opt => opt.MapFrom(
                    src => new UserRegistration { applicationId = src.AppId, roles = src.Roles.ToList() }));

        this.CreateMap<RegistrationResponse, SignUpOutput>()
            .ForMember(dest => dest.UserId, opt => opt.MapFrom(src => src.user.id));
    }
}