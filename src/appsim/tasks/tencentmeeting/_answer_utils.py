import logging
import re
import unicodedata
from decimal import Decimal, InvalidOperation


_ANS_RE = re.compile(r"<ans>\s*(.*?)\s*</ans>", re.IGNORECASE | re.DOTALL)
_NUMBER_RE = re.compile(r"(?<![0-9A-Za-z_.])-?\d+(?:\.\d+)?(?![0-9A-Za-z_.])")


def _normalize_text(value) -> str:
    return unicodedata.normalize("NFKC", str(value)).casefold()


def extract_answer_text(result) -> str:
    """Return the final answer text, preferring content inside <ans> tags."""
    if not result:
        logging.error("Validation failed: missing result object.")
        return ""
    if not isinstance(result, dict):
        logging.error("Validation failed: result is not a dict: %r", type(result))
        return ""
    if "final_message" not in result:
        logging.error("Validation failed: result has no final_message.")
        return ""

    final_message = result.get("final_message")
    if final_message is None:
        logging.error("Validation failed: final_message is None.")
        return ""

    final_message = str(final_message)
    if not final_message.strip():
        logging.error("Validation failed: final_message is empty.")
        return ""

    tag_match = _ANS_RE.search(final_message)
    if tag_match:
        answer = tag_match.group(1).strip()
        if not answer:
            logging.error("Validation failed: <ans> tag is empty.")
            return ""
        logging.info("Extracted answer from <ans> tag: %r", answer)
        return answer

    answer = final_message.strip()
    if not answer:
        logging.error("Validation failed: no answer text to check.")
        return ""
    logging.warning("No <ans> tag found; checking the full final_message.")
    return answer


def answer_contains_any(result, keywords) -> bool:
    answer = extract_answer_text(result)
    if not answer:
        return False

    normalized_answer = _normalize_text(answer)
    expected_terms = [
        str(keyword).strip()
        for keyword in keywords
        if keyword is not None and str(keyword).strip()
    ]
    if not expected_terms:
        logging.error("Validation failed: no expected keywords were provided.")
        return False

    for term in expected_terms:
        if _normalize_text(term) in normalized_answer:
            logging.info("Answer contains expected keyword: %r", term)
            return True

    logging.error("Answer did not contain any expected keyword: %r", expected_terms)
    logging.error("Answer checked: %r", answer)
    return False


def answer_contains_all(result, keywords) -> bool:
    answer = extract_answer_text(result)
    if not answer:
        return False

    normalized_answer = _normalize_text(answer)
    expected_terms = [
        str(keyword).strip()
        for keyword in keywords
        if keyword is not None and str(keyword).strip()
    ]
    if not expected_terms:
        logging.error("Validation failed: no expected keywords were provided.")
        return False

    missing_terms = [
        term for term in expected_terms if _normalize_text(term) not in normalized_answer
    ]
    if missing_terms:
        logging.error("Answer is missing expected keywords: %r", missing_terms)
        logging.error("Answer checked: %r", answer)
        return False

    logging.info("Answer contains all expected keywords: %r", expected_terms)
    return True


def answer_contains_number(result, expected) -> bool:
    answer = extract_answer_text(result)
    if not answer:
        return False

    try:
        expected_number = Decimal(str(expected).strip())
    except (InvalidOperation, AttributeError):
        logging.error("Validation failed: expected number is invalid: %r", expected)
        return False

    normalized_answer = _normalize_text(answer)
    normalized_answer = re.sub(r"(?<=\d),(?=\d)", "", normalized_answer)
    for match in _NUMBER_RE.finditer(normalized_answer):
        try:
            actual_number = Decimal(match.group(0))
        except InvalidOperation:
            continue
        if actual_number == expected_number:
            logging.info("Answer contains expected number: %s", expected_number)
            return True

    logging.error("Answer did not contain expected number: %s", expected_number)
    logging.error("Answer checked: %r", answer)
    return False
