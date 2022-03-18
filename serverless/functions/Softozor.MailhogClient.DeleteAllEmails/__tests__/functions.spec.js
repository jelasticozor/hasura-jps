jest.mock('../settings', () => {
  return {
    function: {
      deleteAll: jest.fn(),
      messages: jest.fn(),
    }
  }
})

const createError = require('http-errors')
const mailhog = require('../settings').function
const deleteAllMessages = require('../deleteAllMessages').function

describe('Softozor.MailhogClient.DeleteAllEmails', () => {
  beforeEach(() => {
    mailhog.deleteAll.mockReset()
  })

  describe('Delete all emails', () => {
    it('throws an Error if the wrong email server host is provided', async () => {
      // Given the wrong email server host is provided
      const expectedErrorMsg = 'Connect ECONNREFUSED wrong-host:8025'
      mailhog.deleteAll.mockImplementation(() => {
        throw new Error(expectedErrorMsg)
      })

      // When I delete all messages
      const input = { }
      const act = async () => await deleteAllMessages(input)

      // Then the error of mailhog.getMessages propagates
      await expect(act).rejects.toThrowError(expectedErrorMsg)
    })

    it('throws an Error if the wrong email server port is provided', async () => {
      // Given the wrong email server port is provided
      const expectedErrorMsg = 'Connect ECONNREFUSED correct-host:8024'
      mailhog.deleteAll.mockImplementation(() => {
        throw new Error(expectedErrorMsg)
      })

      // When I delete all messages
      const input = { }
      const act = async () => await deleteAllMessages(input)

      // Then the error of mailhog.getMessages propagates
      await expect(act).rejects.toThrowError(expectedErrorMsg)
    })

    it('throws a bad request whenever mailhog client returns non-successful status code', async () => {
      // Given the method returns a status code different from 200
      mailhog.deleteAll.mockImplementation(() => {
        return {
          statusCode: 400
        }
      })

      // When I delete all messages
      const input = {}
      const act = async () => await deleteAllMessages(input)

      // Then I get a bad request thrown
      await expect(act).rejects.toThrow(new createError.BadRequest('Unable to delete all messages'))
    })
  })
})
