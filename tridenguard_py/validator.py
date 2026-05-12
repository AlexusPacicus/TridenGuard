from models import ExtractionResult, RadicalType

def validate_extraction(extraction: ExtractionResult, source_text: str) -> dict:
    errors = []
    ungrounded_radicals = []
    source_integrity = True
    source_lower = source_text.lower()

    # Check source integrity
    for rad in extraction.radicals:
        val = rad.value.lower()
        # Busca si al menos los primeros 5 caracteres del valor aparecen en el texto fuente
        if len(val) > 3 and val[:5] not in source_lower:
            errors.append('UNGROUNDED_RADICAL')
            ungrounded_radicals.append({"radical": rad.radical.value, "claimed": rad.value})
            source_integrity = False

    present_types = {r.radical for r in extraction.radicals}

    has_actor = RadicalType.ACTOR in present_types
    has_deontic = RadicalType.DEONTIC in present_types
    has_action = RadicalType.ACTION in present_types
    has_object = RadicalType.OBJECT in present_types
    has_metric = RadicalType.METRIC in present_types
    has_condition = RadicalType.CONDITION in present_types
    has_temporal = RadicalType.TEMPORAL in present_types
    has_spatial = RadicalType.SPATIAL in present_types

    has_r1 = False
    has_r2 = False
    has_r3 = False
    has_r5 = False
    has_r6 = False
    has_r7 = False

    # 8 Atomic Exclusion Rules
    if (has_actor or has_deontic) and not has_action:
        errors.append('R1_SUBJECT_WITHOUT_ACTION')
        has_r1 = True

    if has_action and not has_actor:
        errors.append('R2_ACTION_WITHOUT_SUBJECT')
        has_r2 = True

    if has_object and not has_actor and not has_action:
        errors.append('R3_OBJECT_WITHOUT_REFERENT')
        has_r3 = True

    if has_metric and not has_actor and not has_object:
        errors.append('R4_ORPHAN_METRIC')

    if has_condition and not has_action:
        errors.append('R5_CONDITION_WITHOUT_TRIGGER')
        has_r5 = True

    if has_temporal and not has_actor and not has_action:
        errors.append('R6_TEMPORAL_WITHOUT_ANCHOR')
        has_r6 = True

    if has_spatial and not has_actor and not has_action:
        errors.append('R7_INERT_SPATIAL')
        has_r7 = True

    if has_deontic and not has_action:
        errors.append('R8_DEONTIC_WITHOUT_BEHAVIOR')

    # Remove duplicate errors while preserving order
    unique_errors = []
    for error in errors:
        if error not in unique_errors:
            unique_errors.append(error)

    has_critical = not source_integrity or has_r1 or has_r2 or has_r3
    has_warning = has_r5 or has_r6 or has_r7
    has_unknown = len(unique_errors) > 0 and not has_critical and not has_warning
    has_validated = len(unique_errors) == 0 and source_integrity

    return {
        "errors": unique_errors,
        "error_count": len(unique_errors),
        "source_integrity": source_integrity,
        "ungrounded_radicals": ungrounded_radicals,
        "has_critical": has_critical,
        "has_warning": has_warning,
        "has_unknown": has_unknown,
        "has_validated": has_validated
    }