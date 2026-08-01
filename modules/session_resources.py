"""Official PowerPoint resources for the 16 course sessions."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import streamlit as st

from modules.ui_components import SESSION_MODULE, SESSION_TITLES

PPTX_MIME = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
PRESENTATION_DIRECTORY = Path("assets/session_ppts")


@dataclass(frozen=True, slots=True)
class SessionPresentation:
    """Metadata for one official course presentation."""

    session_number: int
    title: str
    path: Path
    download_name: str
    module_number: int
    description: str

    @property
    def absolute_path(self) -> Path:
        """Return the resolved local path without exposing it in the interface."""
        return (REPOSITORY_ROOT / self.path).resolve()


_FILENAMES = {
    1: "session_01_introduction_why_data_visualization_and_storytelling_matter.pptx",
    2: "session_02_mapping_data_to_visual_forms.pptx",
    3: "session_03_coordinate_systems_axes_and_scales.pptx",
    4: "session_04_color_emphasis_and_visual_attention.pptx",
    5: "session_05_visualizing_amounts_with_a_message.pptx",
    6: "session_06_visualizing_distributions_and_variation.pptx",
    7: "session_07_visualizing_proportions_and_composition.pptx",
    8: "session_08_critiquing_and_reframing_weak_visual_stories.pptx",
    9: "session_09_visualizing_relationships_and_building_insight.pptx",
    10: "session_10_visualizing_time_series_and_change_over_time.pptx",
    11: "session_11_dashboard_storytelling_for_business_audiences.pptx",
    12: "session_12_annotation_titles_captions_and_narrative_flow.pptx",
    13: "session_13_common_pitfalls_in_data_storytelling.pptx",
    14: "session_14_strategy_communication_through_visual_stories.pptx",
    15: "session_15_integrated_storytelling_with_data_workshop.pptx",
    16: "session_16_guest_session_healthcare_data_visualization.pptx",
}

SESSION_PRESENTATIONS: dict[int, SessionPresentation] = {
    number: SessionPresentation(
        session_number=number,
        title=SESSION_TITLES[number],
        path=PRESENTATION_DIRECTORY / filename,
        download_name=filename,
        module_number=SESSION_MODULE[number],
        description=f"Official slide deck for Session {number:02d}: {SESSION_TITLES[number]}.",
    )
    for number, filename in _FILENAMES.items()
}


def get_session_presentation(session_number: int) -> SessionPresentation:
    """Return validated metadata for a session presentation."""
    if isinstance(session_number, bool) or not isinstance(session_number, int):
        raise ValueError("Session number must be an integer from 1 to 16.")
    try:
        return SESSION_PRESENTATIONS[session_number]
    except KeyError as exc:
        raise ValueError("Session number must be from 1 to 16.") from exc


@st.cache_data(show_spinner=False)
def load_presentation_bytes(path_string: str) -> bytes:
    """Read a presentation once and cache its bytes across reruns."""
    path = Path(path_string)
    if path.suffix.lower() != ".pptx":
        raise ValueError("Only PPTX presentation files are supported.")
    return path.read_bytes()


def _safe_presentation_bytes(presentation: SessionPresentation) -> bytes | None:
    """Load presentation bytes with precise, user-safe error handling."""
    path = presentation.absolute_path
    try:
        return load_presentation_bytes(str(path))
    except FileNotFoundError:
        st.error(
            f"The Session {presentation.session_number:02d} presentation is temporarily unavailable.",
            icon="⚠️",
        )
    except PermissionError:
        st.error(
            f"The Session {presentation.session_number:02d} presentation cannot be read.",
            icon="⚠️",
        )
    except OSError as exc:
        st.error(
            f"The Session {presentation.session_number:02d} presentation could not be loaded: {exc}",
            icon="⚠️",
        )
    return None


def render_session_presentation(session_number: int) -> None:
    """Render the correctly matched presentation card on one session page."""
    presentation = get_session_presentation(session_number)
    with st.container(border=True):
        info_col, action_col = st.columns([4, 1.45], vertical_alignment="center")
        with info_col:
            st.markdown("### 📽️ Session Presentation")
            st.markdown(
                f"**Session {presentation.session_number:02d}: {presentation.title}**  \n"
                "Use the official presentation during class or download it for revision."
            )
            st.caption(
                "PPTX · Course presentation by Dr. Alok Tiwari, "
                "Goa Institute of Management."
            )
        with action_col:
            data = _safe_presentation_bytes(presentation)
            if data is not None:
                st.download_button(
                    label=f"Download Session {presentation.session_number:02d} PPT",
                    data=data,
                    file_name=presentation.download_name,
                    mime=PPTX_MIME,
                    key=f"session_ppt_download_{presentation.session_number}",
                    help="Download the official editable PowerPoint presentation.",
                    use_container_width=True,
                )


def render_presentation_library() -> None:
    """Render a responsive, lazy-loading library for all official presentations."""
    st.divider()
    st.header("Course Presentation Library")
    st.write(
        "Official PowerPoint decks are available for every course session. "
        "Choose a session below; only the selected file is loaded."
    )

    selected_key = "presentation_library_selected"
    st.session_state.setdefault(selected_key, 1)

    for start in range(1, 17, 2):
        columns = st.columns(2)
        for column, number in zip(columns, range(start, min(start + 2, 17))):
            presentation = SESSION_PRESENTATIONS[number]
            with column:
                with st.container(border=True):
                    st.markdown(f"#### Session {number:02d}")
                    st.write(presentation.title)
                    st.caption(f"Module {presentation.module_number} · PPTX")
                    if st.button(
                        f"Prepare Session {number:02d} download",
                        key=f"prepare_ppt_{number}",
                        use_container_width=True,
                    ):
                        st.session_state[selected_key] = number

    selected = get_session_presentation(int(st.session_state[selected_key]))
    with st.container(border=True):
        st.subheader(f"Selected: Session {selected.session_number:02d}")
        st.write(selected.title)
        data = _safe_presentation_bytes(selected)
        if data is not None:
            st.download_button(
                label=f"Download Session {selected.session_number:02d} PPT",
                data=data,
                file_name=selected.download_name,
                mime=PPTX_MIME,
                key=f"library_ppt_download_{selected.session_number}",
                help="Download the official editable PowerPoint presentation.",
                use_container_width=True,
            )
        st.caption(
            "Educational course resource. Attribution to Dr. Alok Tiwari and "
            "Goa Institute of Management must be retained."
        )


def render_home_presentation_notice(resources_page: object | None = None) -> None:
    """Add a restrained home-page notice linking to the presentation library."""
    st.info(
        "Official course presentations are available for all 16 sessions. "
        "Open a session to download its corresponding deck or use the "
        "Course Presentation Library.",
        icon="📽️",
    )
    if resources_page is not None:
        st.page_link(
            resources_page,
            label="Open Course Presentation Library",
            icon=":material/slideshow:",
        )
