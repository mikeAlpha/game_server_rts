from typing import List
from typing import Any
from dataclasses import dataclass
import json

@dataclass
class AllCityDatum:
    buildingType: int
    maxStructureCount: int
    createdBuildings: list()
    buildingGenerationData: list()

    @staticmethod
    def from_dict(obj: Any) -> 'AllCityDatum':
        _buildingType = int(obj.get("buildingType"))
        _maxStructureCount = int(obj.get("maxStructureCount"))
        _createdBuildings = [CreatedBuilding.from_dict(y) for y in obj.get("createdBuildings")]
        _buildingGenerationData = BuildingGenerationData.from_dict(obj.get("buildingGenerationData"))
        return AllCityDatum(_buildingType, _maxStructureCount, _createdBuildings, _buildingGenerationData)

@dataclass
class BuildingGenerationData:
    currentStructureCount: int
    isUnLocked: bool
    unlockAtMainBuildingLevel: int
    requiredCurrenciesToEstablish: list()
    buildingGenerationInfoList: list()

    @staticmethod
    def from_dict(obj: Any) -> 'BuildingGenerationData':
        _currentStructureCount = int(obj.get("currentStructureCount"))
        _isUnLocked = ""
        _unlockAtMainBuildingLevel = int(obj.get("unlockAtMainBuildingLevel"))
        _requiredCurrenciesToEstablish = [RequiredCurrenciesToEstablish.from_dict(y) for y in obj.get("requiredCurrenciesToEstablish")]
        _buildingGenerationInfoList = [BuildingGenerationInfoList.from_dict(y) for y in obj.get("buildingGenerationInfoList")]
        return BuildingGenerationData(_currentStructureCount, _isUnLocked, _unlockAtMainBuildingLevel, _requiredCurrenciesToEstablish, _buildingGenerationInfoList)

@dataclass
class BuildingGenerationInfoList:
    mainBuildingLevel: int
    maxStructureCount: int

    @staticmethod
    def from_dict(obj: Any) -> 'BuildingGenerationInfoList':
        _mainBuildingLevel = int(obj.get("mainBuildingLevel"))
        _maxStructureCount = int(obj.get("maxStructureCount"))
        return BuildingGenerationInfoList(_mainBuildingLevel, _maxStructureCount)

@dataclass
class CreatedBuilding:
    worldPos: None
    localScale: None
    maxScale: None
    buildingLevel: int
    totalUpgradeTime: float
    elapsedUpgradeTime: float
    isUpgrading: bool
    isEstablishing: bool

    @staticmethod
    def from_dict(obj: Any) -> 'CreatedBuilding':
        _worldPos = WorldPos.from_dict(obj.get("worldPos"))
        _localScale = LocalScale.from_dict(obj.get("localScale"))
        _maxScale = MaxScale.from_dict(obj.get("maxScale"))
        _buildingLevel = int(obj.get("buildingLevel"))
        _totalUpgradeTime = float(obj.get("totalUpgradeTime"))
        _elapsedUpgradeTime = float(obj.get("elapsedUpgradeTime"))
        _isUpgrading = ""
        _isEstablishing = ""
        return CreatedBuilding(_worldPos, _localScale, _maxScale, _buildingLevel, _totalUpgradeTime, _elapsedUpgradeTime, _isUpgrading, _isEstablishing)

@dataclass
class CurrencySprite:
    instanceID: int

    @staticmethod
    def from_dict(obj: Any) -> 'CurrencySprite':
        _instanceID = int(obj.get("instanceID"))
        return CurrencySprite(_instanceID)

@dataclass
class LocalScale:
    x: float
    y: float
    z: float

    @staticmethod
    def from_dict(obj: Any) -> 'LocalScale':
        _x = float(obj.get("x"))
        _y = float(obj.get("y"))
        _z = float(obj.get("z"))
        return LocalScale(_x, _y, _z)

@dataclass
class MaxScale:
    x: float
    y: float
    z: float

    @staticmethod
    def from_dict(obj: Any) -> 'MaxScale':
        _x = float(obj.get("x"))
        _y = float(obj.get("y"))
        _z = float(obj.get("z"))
        return MaxScale(_x, _y, _z)

@dataclass
class OtherPlayerSaveDatum:
    allCityData: List[AllCityDatum]
    playerData: None

    @staticmethod
    def from_dict(obj: Any) -> 'OtherPlayerSaveDatum':
        _allCityData = [AllCityDatum.from_dict(y) for y in obj.get("allCityData")]
        _playerData = PlayerData.from_dict(obj.get("playerData"))
        return OtherPlayerSaveDatum(_allCityData, _playerData)

@dataclass
class PlayerData:
    freshUser: bool
    userName: str
    selectedLeague: str
    appQuitTime: str

    @staticmethod
    def from_dict(obj: Any) -> 'PlayerData':
        _freshUser = ""
        _userName = str(obj.get("userName"))
        _selectedLeague = str(obj.get("selectedLeague"))
        _appQuitTime = str(obj.get("appQuitTime"))
        return PlayerData(_freshUser, _userName, _selectedLeague, _appQuitTime)

@dataclass
class PlayerSaveData:
    allCityData: List[AllCityDatum]
    playerData: PlayerData

    @staticmethod
    def from_dict(obj: Any) -> 'PlayerSaveData':
        _allCityData = [AllCityDatum.from_dict(y) for y in obj.get("allCityData")]
        _playerData = PlayerData.from_dict(obj.get("playerData"))
        return PlayerSaveData(_allCityData, _playerData)

@dataclass
class RequiredCurrenciesToEstablish:
    currencyIndex: int
    currencyAmount: int
    currencySprite: CurrencySprite

    @staticmethod
    def from_dict(obj: Any) -> 'RequiredCurrenciesToEstablish':
        _currencyIndex = int(obj.get("currencyIndex"))
        _currencyAmount = int(obj.get("currencyAmount"))
        _currencySprite = CurrencySprite.from_dict(obj.get("currencySprite"))
        return RequiredCurrenciesToEstablish(_currencyIndex, _currencyAmount, _currencySprite)

@dataclass
class Root:
    PlayerSaveData: PlayerSaveData
    otherPlayerSaveData: List[OtherPlayerSaveDatum]

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _PlayerSaveData = PlayerSaveData.from_dict(obj.get("PlayerSaveData"))
        _otherPlayerSaveData = [OtherPlayerSaveDatum.from_dict(y) for y in obj.get("otherPlayerSaveData")]
        return Root(_PlayerSaveData, _otherPlayerSaveData)

@dataclass
class WorldPos:
    x: float
    y: float
    z: float

    @staticmethod
    def from_dict(obj: Any) -> 'WorldPos':
        _x = float(obj.get("x"))
        _y = float(obj.get("y"))
        _z = float(obj.get("z"))
        return WorldPos(_x, _y, _z)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)