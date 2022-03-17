jest.mock('../settings', () => {
  return {
    function: {
      messages: jest.fn()
    }
  }
})

const createError = require('http-errors')
const mailhog = require('../settings').function
const {
  getMessages
} = require('../functions')

describe('Softozor.MailhogClient.GetEmails', () => {
  beforeEach(() => {
    mailhog.messages.mockReset()
  })

  describe('Get messages', () => {
    it('throws an Error if the wrong email server host is provided', async () => {
      // Given the wrong email server host is provided
      const expectedErrorMsg = 'Connect ECONNREFUSED wrong-host:8025'
      mailhog.messages.mockImplementation(() => {
        throw new Error(expectedErrorMsg)
      })

      // When I get the messages
      const input = { }
      const act = async () => await getMessages(input)

      // Then the error of mailhog.getMessages propagates
      await expect(act).rejects.toThrowError(expectedErrorMsg)
    })

    it('throws an Error if the wrong email server port is provided', async () => {
      // Given the wrong email server host is provided
      const expectedErrorMsg = 'Connect ECONNREFUSED correct-host:8024'
      mailhog.messages.mockImplementation(() => {
        throw new Error(expectedErrorMsg)
      })

      // When I get the messages
      const input = { }
      const act = async () => await getMessages(input)

      // Then the error of mailhog.getMessages propagates
      await expect(act).rejects.toThrowError(expectedErrorMsg)
    })

    it('calls the mailhog method with its default values when no user input is provided', async () => {
      // Given get messages successfully returns messages
      mailhog.messages.mockImplementation(() => {
        return {
          items: []
        }
      })

      // When I get messages with no input (start, limit)
      const input = { }
      await getMessages(input)

      // Then the default values are passed to the mailhog client lib
      expect(mailhog.messages).toBeCalledWith(0, 50)
    })

    it.each([
      [{ start: -1, limit: 100 }, 'argument "start" cannot be negative'],
      [{ start: 1, limit: -1 }, 'argument "limit" cannot be negative'],
      [{ start: -1, limit: -1 }, 'argument "start" cannot be negative']
    ])('throws a bad request if at least one of the input arguments is negative', async (input, expectedErrorMsg) => {
      // When I get messages with negative input values
      const act = async () => await getMessages(input)

      // Then I get a bad request thrown
      await expect(act).rejects.toThrow(new createError.BadRequest(expectedErrorMsg))
    })
  })
})
