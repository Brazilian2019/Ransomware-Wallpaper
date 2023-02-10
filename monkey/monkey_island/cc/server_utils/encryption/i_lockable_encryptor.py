from abc import ABC, abstractmethod

# NOTE: The ILockableEncryptor introduces temporal coupling, that is, you must first unlock the
#       encryptor before you can use it. This is because the key material used to encrypt repository
#       contents is encrypted using the user's username and password. This adds extra security by
#       allowing us to fully encrypt data at rest. Without this, we'd need to store the repository
#       key in plaintext. Alternative solutions are as follows:
#           1. Store the repository key in plaintext
#           2. Add an initialization phase to the island's boot sequence. At the moment, this is the
#              only element of the design that would benefit from adding an additional phase. If
#              other temporal coupling begins to creep in, we can add the initialization phase at
#              that time and remove this interface.


class LockedKeyError(Exception):
    """
    Raised when an ILockableEncryptor attemps to encrypt or decrypt data before the
    ILockableEncryptor has been unlocked.
    """


class UnlockError(Exception):
    """
    Raised if an error occurs while attempting to unlock an ILockableEncryptor
    """


class ResetKeyError(Exception):
    """
    Raised if an error occurs while attempting to reset an ILockableEncryptor's key
    """


class ILockableEncryptor(ABC):
    """
    An encryptor that can be locked or unlocked.

    ILockableEncryptor's require a secret in order to access their key material. These encryptors
    must be unlocked before use and can be re-locked at the user's request.
    """

    @abstractmethod
    def unlock(self, secret: bytes):
        """
        Unlock the encryptor

        :param secret: A secret that must be used to access the ILockableEncryptor's key material.
        :raises UnlockError: If the ILockableEncryptor could not be unlocked
        """

    @abstractmethod
    def lock(self):
        """
        Lock the encryptor, making it unusable
        """

    @abstractmethod
    def reset_key(self):
        """
        Reset the encryptor's key

        Remove the existing key material so that it can never be used again.

        :raises ResetKeyError: If an error occurred while attemping to reset the key
        """

    @abstractmethod
    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypts data and returns the ciphertext.

        :param plaintext: Data that will be encrypted
        :return: Ciphertext generated by encrypting the plaintext
        :raises LockedKeyError: If encrypt() is called while the ILockableEncryptor is locked
        """

    @abstractmethod
    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypts data and returns the plaintext.

        :param ciphertext: Ciphertext that will be decrypted
        :return: Plaintext generated by decrypting the ciphertext
        :raises LockedKeyError: If decrypt() is called while the ILockableEncryptor is locked
        """
