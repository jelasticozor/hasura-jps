jest.mock('../settings', () => {
  return {
    function: {
      deleteMessage: jest.fn(),
    }
  }
})

const createError = require('http-errors')
const mailhog = require('../settings').function
const {
  deleteMessage,
} = require('../functions')

describe('Softozor.MailhogClient.DeleteEmail', () => {
  beforeEach(() => {
    mailhog.deleteMessage.mockReset()
  })

  describe('Delete message', () => {
    it('throws an Error if the wrong email server host is provided', async () => {
      // Given the wrong email server host is provided
      const expectedErrorMsg = 'Connect ECONNREFUSED wrong-host:8025'
      mailhog.deleteMessage.mockImplementation(() => {
        throw new Error(expectedErrorMsg)
      })

      // When I delete a message
      const input = { id: 'the-message-id' }
      const act = async () => await deleteMessage(input)

      // Then the error of mailhog.getMessages propagates
      await expect(act).rejects.toThrowError(expectedErrorMsg)
    })

    it('throws an Error if the wrong email server port is provided', async () => {
      // Given the wrong email server port is provided
      const expectedErrorMsg = 'Connect ECONNREFUSED correct-host:8024'
      mailhog.deleteMessage.mockImplementation(() => {
        throw new Error(expectedErrorMsg)
      })

      // When I delete a message
      const input = { id: 'the-message-id' }
      const act = async () => await deleteMessage(input)

      // Then the error of mailhog.getMessages propagates
      await expect(act).rejects.toThrowError(expectedErrorMsg)
    })

    it.each([
      [{}],
      [{ id: '' }]
    ])('throws a bad request if the id is null or empty', async input => {
      // Given the method is successful
      mailhog.deleteMessage.mockImplementation(() => {
        return {
          statusCode: 200
        }
      })

      // When I delete a message with null or empty id
      const act = async () => await deleteMessage(input)

      // Then I get a bad request thrown
      await expect(act).rejects.toThrow(new createError.BadRequest('id missing from input'))
    })

    it('throws a bad request whenever mailhog client returns non-successful status code', async () => {
      // Given the method returns a status code different from 200
      mailhog.deleteMessage.mockImplementation(() => {
        return {
          statusCode: 400
        }
      })

      // When I delete a message
      const input = { id: 'the-message-id' }
      const act = async () => await deleteMessage(input)

      // Then I get a bad request thrown
      await expect(act).rejects.toThrow(new createError.BadRequest(`Unable to delete message with id ${input.id}`))
    })

    it('throws a bad request if the email id was not found', async () => {
      // Given the email cannot be found with the supplied id
      mailhog.deleteMessage.mockImplementation(() => {
        return {
          statusCode: 500,
          statusMessage: 'Internal Server Error'
        }
      })

      // When I delete the message
      const input = { id: 'the-message-id' }
      const act = async () => await deleteMessage(input)

      // Then I get a bad request thrown
      await expect(act).rejects.toThrow(new createError.BadRequest(`Unable to delete message with id ${input.id}`))
    })

    it('returns the input id upon success', async () => {
      // Given the method successfully returns
      mailhog.deleteMessage.mockImplementation(() => {
        return {
          statusCode: 200
        }
      })

      // When I delete a message
      const input = { id: 'the-message-id' }
      const response = await deleteMessage(input)

      // Then I get back the deleted message id
      expect(response).toHaveProperty('id')
      expect(response.id).toEqual(input.id)
    })
  })
})
