"""
Tests for the FastAPI application in run.py
These tests specifically target the functions and endpoints implemented in run.py
"""
import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add the parent directory to the path to import run.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from run import app, hello, get_time, soma, create_item, invert, Item
from datetime import datetime


# Create test client for FastAPI app
client = TestClient(app)


def test_hello_endpoint():
    """Test the hello endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_hello_function():
    """Test the hello function directly"""
    result = hello()
    assert result == {"Hello": "World"}


def test_time_endpoint():
    """Test the time endpoint"""
    response = client.get("/time")
    assert response.status_code == 200
    data = response.json()
    assert "current_time" in data
    # Verify it's a valid datetime format
    datetime.fromisoformat(data["current_time"])


def test_get_time_function():
    """Test the get_time function directly"""
    result = get_time()
    assert "current_time" in result
    # Verify it's a valid datetime format
    datetime.fromisoformat(result["current_time"])


def test_soma_endpoint():
    """Test the soma endpoint"""
    response = client.get("/soma?a=5&b=3")
    assert response.status_code == 200
    assert response.json() == {"result": 8}


def test_soma_function():
    """Test the soma function directly"""
    result = soma(5, 3)
    assert result == {"result": 8}


def test_soma_negative_numbers():
    """Test soma with negative numbers"""
    result = soma(-2, 3)
    assert result == {"result": 1}


def test_soma_zero():
    """Test soma with zero"""
    result = soma(0, 5)
    assert result == {"result": 5}


def test_create_item_endpoint():
    """Test the create_item endpoint"""
    item_data = {"name": "test_item", "value": 42}
    response = client.post("/item", json=item_data)
    assert response.status_code == 200
    expected = {"mensagem": "Recebido test_item com valor 42"}
    assert response.json() == expected


def test_create_item_function():
    """Test the create_item function directly"""
    item = Item(name="test_item", value=42)
    result = create_item(item)
    expected = {"mensagem": "Recebido test_item com valor 42"}
    assert result == expected


def test_invert_endpoint():
    """Test the invert endpoint"""
    response = client.get("/invert?texto=hello")
    assert response.status_code == 200
    assert response.json() == {"invertido": "olleh"}


def test_invert_function():
    """Test the invert function directly"""
    result = invert("hello")
    assert result == {"invertido": "olleh"}


def test_invert_empty_string():
    """Test invert with empty string"""
    result = invert("")
    assert result == {"invertido": ""}


def test_invert_palindrome():
    """Test invert with palindrome"""
    result = invert("aba")
    assert result == {"invertido": "aba"}


def test_invert_special_characters():
    """Test invert with special characters"""
    result = invert("hello, world!")
    assert result == {"invertido": "!dlrow ,olleh"}